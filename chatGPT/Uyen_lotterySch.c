#include "types.h"
#include "param.h"
#include "memlayout.h"
#include "riscv.h"
#include "spinlock.h"
#include "proc.h"
#include "defs.h"

struct cpu cpus[NCPU];

struct proc proc[NPROC];

struct proc *initproc;

int nextpid = 1;
struct spinlock pid_lock;

extern void forkret(void);
static void freeproc(struct proc *p);

extern char trampoline[]; // trampoline.S

// helps ensure that wakeups of wait()ing
// parents are not lost. helps obey the
// memory model when using p->parent.
// must be acquired before any p->lock.
struct spinlock wait_lock;

///...... some code here

// lottery scheduler
// we need to access function srand() from sysproc.c
extern int sys_srand(void);

// helper struct to keep track of range for each proc
struct range_proc
{
    int range_start;
    int range_end;
    struct proc *proc;
};

void scheduler(void)
{
    struct proc *p;
    struct cpu *c = mycpu();
    int total_tickets = 0;
    int ticket_ranges[NPROC][2];
    // ticket_ranges[NPROC][2] mean the range of tickets for each process
    struct range_proc range_procs[NPROC];
    int i;
    int rand_num = 0;
    struct proc *winnerProc = 0;

    c->proc = 0;
    sys_srand(); // Seed the random number generator

    for (;;)
    {
        // Avoid deadlock by ensuring that devices can interrupt.
        intr_on();

        // Calculate total tickets and assign ticket ranges
        total_tickets = 0;
        for (i = 0, p = proc; p < &proc[NPROC]; i++, p++)
        {
            if (p->state != UNUSED)
            {

                // Assign ticket range
                ticket_ranges[i][0] = total_tickets;
                ticket_ranges[i][1] = total_tickets + p->tickets - 1;
                total_tickets += p->tickets;

                // Store process pointer with range
                range_procs[i].range_start = ticket_ranges[i][0];
                range_procs[i].range_end = ticket_ranges[i][1];
                range_procs[i].proc = p;
            }
        }

        // If no runnable processes, skip
        if (total_tickets != 0)
        {

            // Pick a random number
            // and we mod the number by total_tickets
            // bc we want the number to be within the range of total_tickets
            rand_num = sys_srand() % total_tickets;

            // Find the winner
            for (i = 0; i < NPROC; i++)
            {
                // if not good
                if (range_procs[i].proc == 0 || range_procs[i].proc->state != RUNNABLE)
                    continue;

                // Check if winner
                if (rand_num >= range_procs[i].range_start && rand_num <= range_procs[i].range_end)
                {

                    // print winning number and range to verify that it work
                    // printf("Winning number and range: %d, %d-%d\n", rand_num, range_procs[i].range_start, range_procs[i].range_end);
                    winnerProc = range_procs[i].proc;
                    break;
                }
            }
        }

        // If no winner, skip otherwise switch to winner
        if (winnerProc != 0)
        {
            // printf("have winner\n");
            //  Switch to chosen process
            acquire(&winnerProc->lock);
            if (winnerProc->state == RUNNABLE)
            {
                // printf("runnable\n");
                //   Update ticket ranges if process completed
                //   if (winnerProc->state == UNUSED)
                //{
                //  printf("unused\n");
                for (i = 0; i < NPROC; i++)
                {
                    // recheck again
                    if (proc[i].state != UNUSED)
                    {
                        // printf("1\n");
                        //  ticket_range[i][0] mean the lower bound of the ticket range
                        //  and if lower bound is greater than the winner's upper bound
                        //  then we need to subtract winner's ticket from the lower bound
                        if (ticket_ranges[i][0] > ticket_ranges[winnerProc->pid][1])
                        {
                            // printf("2\n");
                            ticket_ranges[i][0] -= winnerProc->tickets;
                            ticket_ranges[i][1] -= winnerProc->tickets;
                        }
                        // ticket_range[i][1] mean the upper bound of the ticket range
                        // and if upper bound is less than the winner's lower bound
                        else if (ticket_ranges[i][1] < ticket_ranges[winnerProc->pid][0])
                        {
                            // printf("3\n");
                            //  Do nothing
                        }
                        // if winner's ticket range is within the range of another process
                        // then we need to remove the winner's ticket range
                        // by setting the range to -1
                        else if (ticket_ranges[i][0] >= ticket_ranges[winnerProc->pid][0] && ticket_ranges[i][1] <= ticket_ranges[winnerProc->pid][1])
                        {
                            // printf("4\n");
                            ticket_ranges[i][0] = -1;
                            ticket_ranges[i][1] = -1;
                        }
                        // if winner's ticket range is partially within the range of another process
                        // then we need to update the range
                        else if (ticket_ranges[i][0] < ticket_ranges[winnerProc->pid][0] && ticket_ranges[i][1] > ticket_ranges[winnerProc->pid][1])
                        {
                            // printf("5\n");
                            ticket_ranges[i][1] -= winnerProc->tickets;
                        }
                        else if (ticket_ranges[i][0] < ticket_ranges[winnerProc->pid][0])
                        {
                            // printf("6\n");
                            ticket_ranges[i][1] = ticket_ranges[winnerProc->pid][0] - 1;
                        }
                        else if (ticket_ranges[i][1] > ticket_ranges[winnerProc->pid][1])
                        {
                            // printf("7\n");
                            ticket_ranges[i][0] = ticket_ranges[winnerProc->pid][1] + 1;
                        }
                        // just to catch weird case not work
                        else
                        {
                            // printf("8\n");
                            ticket_ranges[i][0] = -1;
                            ticket_ranges[i][1] = -1;
                        }
                    }
                }
                //}

                // Switch to chosen process
                winnerProc->state = RUNNING;
                c->proc = winnerProc;
                swtch(&c->context, &winnerProc->context);
                c->proc = 0;
                // print winner num
                // printf("winner num: %d\n", rand_num);
            }
            release(&winnerProc->lock);
        }
    }
}

///...... some code here
