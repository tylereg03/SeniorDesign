@bot.command(name='top5')
async def top5(ctx, arg):
    """
    A Discord bot command to fetch and display the top 5 songs of a specified artist.

    Parameters:
    - ctx (commands.Context): The context object representing the command invocation.
    - arg (str): The argument passed with the command, representing the artist's name.

    Returns:
    - None: Sends messages to the Discord channel with the top 5 songs of the artist or appropriate error messages.
    """

    # Convert the artist name argument to uppercase
    arg = arg.upper()

    # Search for the artist using the Spotify API
    result = sp.search(q=f'artists: {arg}', type='artist', limit=50, market=None)

    # If no results are found, try searching with the artist name in lowercase
    if result['artists']['total'] == 0:
        arg = arg.lower()
        result = sp.search(q=f'artists: {arg}', type='artist', limit=50, market=None)

    # If still no results, exit the function
    if not result['artists']['items']:
        return

    # Initialize variables to store the found artist's ID and name
    artist_id = None
    artist_name = None

    # Loop through the search results to find a matching artist with popularity above 40
    for artist in result['artists']['items']:
        if (artist['name'].lower() == arg or artist['name'].upper() == arg) and int(artist['popularity']) > 40:
            artist_name = artist['name']
            artist_id = artist['id']
            break

    # If no matching artist is found, send an error message
    if artist_id is None:
        await ctx.send(f"No artist found with the name '{arg}'.")
    else:
        # Fetch the top tracks of the found artist from the Spotify API
        top_tracks = sp.artist_top_tracks(artist_id, country='US')

        # If no top tracks are found, send an error message
        if not top_tracks['tracks']:
            await ctx.send("No top tracks found for the artist.")
        else:
            # Display the top 5 songs for the artist
            await ctx.send(f"Top 5 songs for the artist {artist_name}:")
            for i, track in enumerate(top_tracks['tracks'][:5]):
                await ctx.send(f"{i + 1}. {track['name']} - {', '.join(artist['name'] for artist in track['artists'])}")
            return
