# README

postmigrator.py is a tool to help migrate backed up posts from Live Journal blog.
I used a tool called [Charm](http://sourceforge.net/projects/ljcharm/) to back up posts from my livejournal, but needed something to convert them into markdown,
to then feed jekyll, to get the resultant HTML content for my site, and postmigrator was the result.

# Usage
1. Run ljcharm and choose appropriate options to decide on how many/which posts you want to migrate. 
You can refer to the [manual for ljcharm, detailing the options.](http://ljcharm.sourceforge.net/manual.html)
2. Create a directory and place the directory containing the files retrieved using ljcharm, into it. Do not have any other files (other than the files present in this repo, and the retrieved posts directory) in this directory.
3. Execute postmigrator.py. Metadata entries are preserved/converted for date, title, mood, and music. 
4. Tags from the old blogs may or may not be relevant, so the original tags get replaced by a single 'archived-posts' tag, by default; if you wish to retain the original tags, use the  --retain-tags option.
5. If you wish additional fields to be added to the YAML front-matter in the resulting markdown files, add them into addl_metadata
6. postmigrator respects the security/visibility settings present in the original blog posts; general posts are present in the output directory, and custom, friends, and private posts are written into the respectively named directories, under output.
