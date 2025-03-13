* Add data on when songs were added to playlist
* Create models/tables for songs and playlists to cache
  * Making multiple api calls for every page load is not feasible
  * Tables:
    * playlist (trimmed_playlist params + last_updated)
    * playlist_item (trimmed_track params, playlist_id, last_updated)
  
* Implement function that will check and update playlists at some regular interval
* Spotify search
* Allow editing of playlists
* Create a more intelligent search function
   * Integrate a lyrics api to allow for full text search?
   * Allow searching by artist, album, song name
   * Allow searching by genre, release date, etc.
