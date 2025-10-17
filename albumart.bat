SET filename=%~1
cd "S:\Streaming\Stream assets\FB2KNowPlayingOverlay\"
if exist "%filename%\folder.jpg" (	
    copy "%filename%\folder.jpg" albumart.jpg
) else (
    copy noart.jpg albumart.jpg
)