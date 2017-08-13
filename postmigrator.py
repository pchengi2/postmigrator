#!/usr/bin/env python
import os,re,datetime,sys


def reformat_fields(line,frontmatter,filename,security):
	
	test=line.split(' ')[0]
	if test.find(':') == -1:
		return(1,frontmatter,filename,security)
	pline=re.sub(r'( )(\1+)', r'\1', line).split('\n')[0]
	if test == 'Date:':
		vals=pline.split(' ')
		mix=vals[1]+' '+vals[2]
		dt=datetime.datetime.strptime(mix,'%Y-%m-%d %H:%M')
		dts=datetime.datetime.strftime(dt,'%Y-%m-%d %H:%M:%S')
		fdatestr=datetime.datetime.strftime(dt,'%Y-%m-%d-')
		repl='date:	'+dts
		frontmatter+=repl+'\n'
		filename=fdatestr
		return(0,frontmatter,filename,security)
	rhs=pline.split(':')
	key=rhs.pop(0)
	recombined=''
	for el in rhs:
		recombined+=el
	val=re.sub('[:!@#$\']','', recombined)
	if key == 'Tags':
		repl='tags: ['
		rtags=val.lstrip().split(',')
		for rtag in rtags:
			cleaned=re.sub('[!@#$ \']','-', rtag.lstrip())
			repl+=cleaned
			repl+=','
		repl+=']\n'
		repl='tags: [archived-posts]\n'
		frontmatter+=repl
		return(0,frontmatter,filename,security)
	if key == 'Subject':
		repl='title: '+val+'\n'
		repl=re.sub('[\'\"]','', repl)
		frontmatter+=repl
		filename+=re.sub('[!@#$/*?|;,\t \'\"]','-',val.lstrip())
		filename=re.sub('[.]','',filename)+'.md'
		return(0,frontmatter,filename,security)

	if key == 'Mood':
		repl='mood: '+val+'\n'
		return(0,frontmatter,filename,security)

	if key == 'Security':
		security+=val.lstrip().split('\n')[0]
		return(0,frontmatter,filename,security)

	return(0,frontmatter,filename,security)

flist=list()

for dirs in  ['output/custom','output/friends','output/private']:
	if not os.path.exists(dirs):
		os.makedirs(dirs)
exclude=set(['output','backup','.git'])
for path, subdirs, files in os.walk('.'):
	subdirs[:] = [d for d in subdirs if d not in exclude]
	for name in files:
		if name == 'postmigrator.py' or name == 'README.md' or name == '.gitignore':
			continue
		flist.append(os.path.join(path,name))

for fn in flist:
	with open(fn,'r') as f:
		lines=f.readlines();
	foundall=0
	outp=''
	filename='garbage'
	security='output/'
	frontmatter='---\n'+'layout: post\n'
	for line in lines:
		if foundall == 0:
			retval,frontmatter,filename,security=reformat_fields(line,frontmatter,filename,security)
			if retval == 1:
				foundall=1
				frontmatter+='categories: archives\n'
				frontmatter+='permalink: /:categories/:year/:month/:day/:title/\n'
				outp=frontmatter
				outp+='---\n'
				print outp
				print filename
				if filename == 'garbage':
					print 'file is '+fn
			continue
		line=re.sub('<p>','',line)
		line=re.sub('</p>','',line)
		outp+=line
	finalfn=security+'/'+filename
	if not os.path.exists(security):
		os.makedirs(security)
	with open(finalfn,'w') as f:
		f.write(outp)
	
