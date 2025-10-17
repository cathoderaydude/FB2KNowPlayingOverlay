SET filename=%~1
cd /D "C:\Code\FB2KNowPlayingOverlay\"
echo "%filename%" > albumart.txt
if exist "%filename%\folder.jpg" (	
    copy "%filename%\folder.jpg" albumart.jpg
) else (
    if exist "%filename%\cover.jpg" (
		copy "%filename%\cover.jpg" albumart.jpg
	) else (
		if exist "%filename%\front.jpg" (
			copy "%filename%\front.jpg" albumart.jpg
		) else (
			copy noart.jpg albumart.jpg
		)
	)
)
pause