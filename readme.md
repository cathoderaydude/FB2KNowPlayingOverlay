# foobar2000 Now Playing overlay for OBS

This is a moderately-janky solution for getting a Now Playing overlay to appear in your OBS layout. It isn't perfect by a long shot, but if you just want to _play files from your hard drive_ and have the track info appear in OBS, this will solve your problem.

## Pros:

* Works locally. Doesn't require Spotify, iTunes, Youtube Music, Roon, or some online scrobbling service.
* You can modify it pretty easily.
* Visuals can be adjusted a little bit for different scenes
* Can be set to fade in for a few seconds on track changes, then disappear
  * Fade interval is adjustable per-scene
* Displays the track length / elapsed time live
* Displays a live "scrub bar" showing the position in the track
* Displays album art on a good day

## Cons:

* Only works with foobar2000, which is (imo) becoming moribund.
  * For the above reason, it only works on Windows
* Requires a fb2k plugin which will probably evaporate at any moment
* Requires Python to be installed
* Fiddly setup that involves editing files and entering a bunch of hard paths.

Despite these problems, I could not find any better solution. Local media players are virtually a dead product; the only alternative was VLC, whose scripting interface is so godawful that it can't even deliver the bare minimum requirements for this.

# Installation

* Download the package from the Releases section
* Extract it to a folder somewhere on your PC.
  * We will assume you used `C:\Code\FB2KNowPlayingOverlay`
* Install the foobar2000 plugin [Now Playing 2](https://github.com/foxx1337/foo_nowplaying2)
* Make sure you have Python installed. The latest version of python3 should be fine.
  * I recommend running the installer as Administrator and telling it to install systemwide rather than for just your user.

## Configuring foobar

* Open foobar2000 and select **Preferences** from the **File** menu
* Locate **Now Playing 2** under the **Tools** section
* On the **Now Playing** tab, set the **File** value
  * The file is "nowplaying.json", in the folder where you extracted this package.
  * Ex: `C:\Code\FB2KNowPlayingOverlay\nowplaying.json`
* Under the **Format** section, check all the boxes next to **Events**
* Now, paste the following into the text field below those checkboxes:

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
		"path": "$replace($directory_path(%path%),'"','\"','\','\\')"
	}
}
```

* Click OK
* Start playing a song (make sure it has valid artist/track tags!)
* Check in the project directory and make sure `nowplaying.json` has appeared.
* If you want album art, follow the next section; otherwise, jump to **Configuring Overlay**

### Enabling album art

Album art is an egregious hack, so please be aware: **It only works if the art is stored as a file called folder.jpg in the same directory as the song you're playing.** While foobar recognizes other names for album art, there is absolutely no way to determine which file it picked. So if you want this to work reliably, you'll have to go through all your music folders and make sure the album cover has that exact filename.

* Open the **Now Playing 2** config in foobar again.
* Go to the **Log** tab
* Pick a nonsense filename somewhere, it doesn't matter where.
  * If you don't do this, the plugin won't fill in the necessary variable.
* In the **Format** field, enter: `$directory_path(%path%)`
* Go to the **Run** tab
* Ensure **On New Track** is selected.
* In the **Launch** field, enter: `C:\Code\FB2KNowPlayingOverlay\albumart.bat "$np2_log"`
  * As usual, change the folder name if you didn't extract to that exact location.
* Click OK
* Play a new song (one which you know has album art!)
* Look in the project folder and see if an "albumart.jpg" has appeared.
  * If there's no such file _at all_, then the batch file failed to execute. Check the path you entered in the Launch command.
  * If the file is there, open it. If it's a generic CD icon, then the source file was not found; check that "folder.jpg" exists in the same folder as the song you played.
  * If the file is there and has the correct artwork, you're set to jet.

## Setting up the overlay

First, let's start the server and make sure it works.

* Open the folder where you extracted this project
* Launch `runserver.bat`
* A window should appear saying that a server is now running
  * A note of caution: This web server shares everything in the folder it's run from. Make ABSOLUTELY certain you do not put anything private in the same folder!
* Open your web browser and go to `http://localhost:8005/nowplaying.html`
* You should see the Now Playing overlay.
* Play a song in foobar
* The overlay should smoothly update with the new track info.
* Now, open OBS Studio
* Create a **Browser Source**
* Point it to the same URL: `http://localhost:8005/nowplaying.html`
* The Now Playing box should appear on your stream.
* You're ready to go!

# Customizing the overlay

There are several built-in adjustments you can make by modifying the URL in the Browser Source. This allows you to put different versions of the overlay in different scenes. To enable each one, add it to the URL in the browser source in standard HTTP notation, like this:

`http://localhost:8005/nowplaying.html?art=true&fade=true&width=500`

**Album art display:** This is **off** by default. Add `art=true` to enable it.
**Fade out:** This is **off** by default. Add `fade=true` to enable it.
**Fade out delay:** This is 10 seconds by default. Add `fadetime=20` to change it to i.e. 20 seconds.
**Display width:** The UI is about 350 pixels wide by default. Add `width=500` to make it i.e. 500 pixels.

# Credits

This is forked from a project by [farpenoodles](https://github.com/farpenoodle/FB2KNowPlayingOverlay) which had not been updated in over a decade and was so code-rotted that it no longer functioned (e.g. it depended on javascript loaded from a local file being able to access files directly on the host filesystem.) I have rewritten a good chunk of it, but I would not have started the project at all without their framework.
