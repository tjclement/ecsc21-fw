import term, orientation, system, time, uos, json, machine

system.serialWarning()
term.header(True, "Picture")
print("Loading...")

pictures = []

files = uos.listdir('/media')
for f in files:
	if f.endswith('.png'):
		pictures.append("/media/"+f)

try:
	apps = uos.listdir('/lib')
	for app in apps:
		files = uos.listdir('/lib/'+app)
		for f in files:
			if f.endswith('.png'):
				pictures.append("/lib/"+app+"/"+f)
except:
	pass

current = machine.nvs_getstr('splash', 'logo')

while True:
	options = []
	for f in pictures:
		title = f
		if f == current:
			title += " [Enabled]"
		options.append(title)
	options.append("Default logo")
	options.append("< Exit")

	selected = term.menu("Picture", options, 0, "")
	if selected > len(pictures):
		system.home(True)
	if selected == len(pictures):
		current = None
		try:
			machine.nvs_erase("splash", "logo")
		except:
			pass
		term.header(True, "Picture")
		print("Default picture selected")
		
		time.sleep(1)
	else:
		current = pictures[selected]
		machine.nvs_setstr('splash', 'logo', current)
		term.header(True, "Picture")
		print("Selected "+current)
		time.sleep(1)
