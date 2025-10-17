# foobar2000 Now Playing overlay for OBS

![Demo screenshot of the overlay](doc-images/overlay.png?raw=true)

This is a moderately-janky solution for getting a Now Playing overlay to appear in your OBS layout. It isn't perfect by a long shot, but if you just want to _play files from your hard drive_ and have the track info appear in OBS, this will solve your problem.

## Pros:

* Works locally.
* Doesn't require Spotify, iTunes, Youtube Music, Roon, or some online scrobbling service.
* Several customizable visual settings
  * These can be tweaked per-scene if you like
* Can be set to fade in for a few seconds (adjustable) on track changes, then disappear
* Displays the track length / elapsed time live
* Displays a live "scrub bar" showing the position in the track
* Displays album art
  * Will extract album art from files if present
  * Otherwise looks for art in same folder as track

## Cons:

* Only works with foobar2000, which is (imo) becoming moribund.
* Requires a fb2k plugin which may evaporate at any moment, as several others have
	* For the above reasons, it only works on Windows
* Fiddly setup.

Despite these problems, I could not find any better solution. Local media players are virtually a dead product; the only real alternative with any uptake is VLC, which I do not like, and the leading overlay for use with it is Tuna, which doesn't really fit my visual / layout needs and desires. So I built my own thing; maybe it'll also work for you.

# Installation

1. Install foobar2000.
3. Download this project from the **Releases** section
4. Extract it to a folder somewhere on your PC.
	* We will assume you used `C:\Code\FB2KNowPlayingOverlay`
	* If you put it somewhere else, remember to change this in later steps!
5. Install the foobar2000 plugin [Now Playing 2](https://github.com/foxx1337/foo_nowplaying2)
6. Install Python
	* I recommend running the installer as Administrator and telling it to install systemwide rather than for just your user.
 	* If you have problems launching the server or getting the album art to work, this might be why.
7. Open a command prompt
8. Type `pip install TinyTag`
9. Type `pip install Pillow`

All the components are now installed.

## Configuring foobar

1. Open foobar2000 and select **Preferences** from the **File** menu
2. Locate **Now Playing 2** under the **Tools** section
3. On the **Now Playing** tab, set the **File** value:
	* Enter "nowplaying.json", in the folder where you extracted this package.
	* Ex: `C:\Code\FB2KNowPlayingOverlay\nowplaying.json`
4. Under the **Format** section, check all the boxes next to **Events**
5. Now, paste the following into the text field below those checkboxes:

```
{
	"nowplaying": {
		"playing": $replace(%isplaying%,'?','0'),
		"paused": $replace(%ispaused%,'?','0'),
		"albumartist": "$replace(%album artist%,'"','\"','\','\\')",
		"album": "$replace(%album%,'"','\"','\','\\')",
		"artist": "$replace(%artist%,'"','\"','\','\\')",
		"title": "$replace(%title%,'"','\"','\','\\')",
		"tracknumber": $add($replace(%track number%,'?','0'),0),
		"length": $replace(%length_seconds%,'?','0'),
		"elapsed": $replace(%playback_time_seconds%,'?','0'),
		"path": "$replace(%path%,'"','\"','\','\\')"
	}
}
```

The result should look like [this](doc-images/np2-step1.png).

6. Click OK
7. Start playing a song
8. Check in the project directory and make sure `nowplaying.json` has appeared.
9. If you want album art, follow the next section; otherwise, jump to **Configuring Overlay**

### Enabling album art

If you don't want album art, ever, you can skip this section, just remember to disable it in the customization section.

1. Open the **Now Playing 2** config in foobar again.
2. Go to the **Log** tab
3. Select a nonsense filename somewhere, it doesn't matter where.
	- This file is not used for anything, it just enables this feature.
5. In the **Format** field, enter: `%path%` [like this](doc-images/np2-step2.png).
6. Go to the **Run** tab
7. Ensure **On New Track** is checked.
8. In the **Launch** field, enter: `C:\Code\FB2KNowPlayingOverlay\albumart.bat "$np2_log"` [like this](doc-images/np2-step3.png).
	* As usual, change the folder name if you didn't extract to that exact location.
8. Click OK
9. Play a new song (one which you know has album art!)
10. Look in the project folder and see if an "albumart.jpg" has appeared.
	* If there's no such file _at all_, then the script failed to execute. Check the path you entered in the Launch command.
	* If the file is there, but it's a generic CD icon, then the source file was not found; see "Troubleshooting."
	* If the file is there and has the correct artwork, you're set to jet.

## Setting up the overlay

First, let's start the server and make sure it works.

1. Open the folder where you extracted this project
2. Launch `runserver.bat`
3. A window should appear saying that a server is now running
	* A note of caution: This web server shares everything in the folder it's run from. Make ABSOLUTELY certain you do not put anything private in the same folder!
4. Open your web browser and go to `http://localhost:8005/nowplaying.html`
5. You should see the Now Playing overlay.
6. Play a song in foobar
7. The overlay should smoothly update with the new track info.
8. Now, open OBS Studio
9. Create a **Browser Source**
10. Point it to the same URL: `http://localhost:8005/nowplaying.html`
11. The Now Playing box should appear on your stream.
12. You're ready to go!

# Customizing the overlay

There are several built-in adjustments you can make by modifying the URL in the Browser Source. This allows you to put different versions of the overlay in different scenes. To enable each one, add it to the URL in the browser source in standard HTTP notation, like this:

`http://localhost:8005/nowplaying.html?noart=true&fade=true&width=500`

**Album art display:** This is **on** by default. Add `noart=true` to disable it.

**Fade out:** This is **off** by default, so the UI will **always** be visible. Add `fade=true` to make it fade out after each track change.

**Fade out delay:** This is 10 seconds by default. Add `fadetime=20` to change it to i.e. 20 seconds.

**Display width:** The UI is about 500 pixels wide by default. Add i.e. `width=700` to make it 700 pixels.

**Folder name as artist:** If you play a song with no artist tag, the artist field will be blank. If you set `foldername=true` however, the artist field will show the name of the folder the file is in. Be careful if you sometimes store your music in _"C:\FilthyImagesDontLookInHere"_.

**Filename as artist:** As above, except the artist field will show the name of the file itself. Set `filename=true` to enable this.

**Recently played list:** Set `lastplayed=5` to display a list of the last 5 songs played. Note that this will make the UI taller, so after you pick a list size, play enough songs to fill up the whole list, then adjust your OBS browser source to fit or it'll get cut off.

# Troubleshooting

## Album art isn't loading / wrong album art is loading

Album art is retrieved in two different ways:

**Extracted from the song file itself:**
Music from most stores (bandcamp, etc.) has the album art embedded. Assuming you installed TinyTag and Pillow as instructed, this should work automatically. However, some songs don't have it embedded, in which case it has to be...

**Found in a file next to the song itself:**
For this to work, the art must be in the same folder as the song, with one of these names:
	* **front.jpg**
 	* **cover.jpg**
    * **folder.jpg**
    * **[the name of the folder].jpg**

If none of these are found, well, it won't work, naturally. Also, if several of these files exist, they'll be used in the above order, so if you're getting the wrong art, it might be because front.jpg is overriding cover.jpg, in which case the only solution is to delete it.

Also, any art embedded in a file will always override art found in the folder.

# Credits

This is based on a project by [farpenoodles](https://github.com/farpenoodle/FB2KNowPlayingOverlay) which had not been updated in over a decade and was so code-rotted that it no longer functioned (e.g. it depended on javascript loaded from a local file being able to access files directly on the host filesystem.)

I have rewritten essentially all of it, but I would not have started this project at all without their efforts.
