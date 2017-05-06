
def findDuplicates(fileName):
	print('Finding Duplicate tracks in %s...' % fileName);
	# read in a playlist
	plist = plistlib.readPlist(fileName)
	# get the tracks from the Tracks dictionary
	tracks = plist['Tracks']
	# create a track name dictionary
	trackNames = {}
	# iterate through the tracks
	for trackId, track in tracks.items():
		try:
			name = track['Name']
			duration = track['Total Time']
			# look for existing entries
			if name in trackNames:
                # if a name and duration match, increment the count
                # round the track length to the nearest second
				if duration//1000 == trackNames[name][0]//1000:
					count = trackNames[name][1]
					trackNames[name] = (duration, count + 1) 
			else:
				# add dictionary entry as tuple (duration, count)
				trackNames[name] = (duration, 1)
		except:
			# ignore
			pass
	# store duplicates as (name, count) tuples
	dups = []
	for k, v in trackNames.items():
		if v[1] > 1:
			dups.append((v[1], k))
	# save duplicates to a file
	if len(dups) > 0:
		print("Found %d duplicates. Track names saved to dup.txt" % len(dups))
	else:
		print("No duplicate tracks found!")
	f = open("dup.txt", "w")
	for val in dups:
		f.write("[%d] %s\n" % (val[0], val[1]))
	f.close()



def findCommonTracks(fileNames):
	# a list of sets of track names
	trackNameSets = []
	for fileName in fileNames:
		# create a new set
		trackNames = set()
		# read in playlist
		plist = plistlib.readPlist(fileName)
		# get the track
		tracks = plist['Tracks']
		# iterate through the tracks
		for trackId, track in tracks.items():
			try:
				# add a track name to a set
				trackNames.add(track['Name'])
			except:
				# ignore
				pass
		# add to list
		trackNameSets.append(trackNames)
	# get a set of common tracks
	commonTracks = set.intersection(*trackNamesSets)
	# write to file
	if len(commonTracks) > 0:
		f = open("common.txt", "w")
		for val in commonTracks:
			s = "%s\n" % val
			f.write(s.encode("UTF-8"))
		f.close()
		print("%d common tracks found. "
			  "Track names written to common.txt" % len(commonTracks))
	else:
		print("No common tracks!")



def plotStats(fileName):
	# read in a playlist
	plist = plistlib.readPlist(fileName)
	# get the tracks from the playlist
	tracks = plist['Tracks']
	# create lists of song ratings and track durations
	ratings = []
	durations = []
	# iterate through the tracks
	for trackId, track in tracks.items():
		try:
			ratings.append(track['Album Rating'])
			durations.append(track['Total Time'])
		except:
			# ignore
			pass

	# ensure that valid data was collected
	if ratings == [] or durations == []:
		print("No valid Album Rating/Total Time data in %s." % fileName)
		return



def main():
	# create parser
	descStr = """
	This program analyzes playlist files(.xml) exported from Itunes.
	"""
	parser = argparse.ArgumentParser(description=descStr)
