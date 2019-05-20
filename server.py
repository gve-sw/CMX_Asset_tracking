#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from flask import Flask, render_template, flash, request, redirect, url_for, send_file
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField
import json

 
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


 
class GroupTag_Form(Form):
	group = SelectField('Group', choices=[('',''),('G1', 'Group 1'), ('G2', 'Group 2'), ('A', 'ALL Groups')], validators=[validators.required()]) #can be created from the dict ?
	tag = SelectField('Tag', choices=[('',''),('0', 'C4CB6B600C13'),('1', 'C4CB6B600CC3'),('2', 'C4CB6B600CBF')], validators=[validators.required()])
 
class Select_Form(Form):
	group = SelectField('Group', choices=[('',''),('G1', 'Group 1'), ('G2', 'Group 2'), ('A', 'ALL Rooms')]) 
	tag = SelectField('Tag', choices=[('',''),('0', 'C4CB6B600C13'),('1', 'C4CB6B600CC3'),('2', 'C4CB6B600CBF')])



@app.route("/start", methods=['GET'])
def start():
	formgroup = GroupTag_Form()
	formselect = Select_Form()
	status=request.args.get('status')
	tag_data = json.loads(open('js/nodes.js').read())['all_nodes']
	creat_topology(status,tag_data)
	return render_template('index.html', formgroup=formgroup, formselect=formselect , status=status)

@app.route("/topology", methods=['GET'])
def topology():
	html = render_template('topology.html')
	return html

@app.route("/add_tag_to_group", methods=['POST'])
def add_port_to_room():
	form = GroupTag_Form(request.form)
	#print form.errors
	if request.method == 'POST':

		tag=request.form['tag']
		group=request.form['group']
 
		if form.validate():
			f_add_port_to_room(tag,group)
			creat_topology(status,tag_data)
			flash('Asset succefully added to group'+port,'OK')

		else:
			flash('All the form fields are required.','ERROR')

	return redirect(url_for('start',status='PRT'))


@app.route("/select", methods=['POST'])
def select():
	form = Select_Form(request.form)
	#print form.errors
	if request.method == 'POST':
		tag=request.form['tag']
		group=request.form['group']
		if form.validate():
			nodes_data = json.loads(open('js/nodes.js').read())
			groups_data = json.loads(open('js/rooms.js').read())
			nodes_list=[]
			if tag!='':
				for node in nodes_data['all_nodes']:
					if str(node['id']) == str(tag):
						nodes_list.append(node)
						creat_topology('Action',nodes_list)
			elif group!='':				
				for node in nodes_data['all_nodes']:
					if node['id'] in groups_data["Groups"][group] :
						nodes_list.append(node)
				creat_topology('Action',nodes_list)				
			flash('Asset succefully located'+tag,'OK')
		else:
			flash('at least one form fields required.','ERROR')
	return redirect(url_for('start',status='VLAN'))

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['Cache-Control'] = 'no-cache'
    return response

@app.route('/floor_image')
def get_image():
    return send_file('static/img/maping.png', mimetype='image/gif')

@app.route("/webhook", methods=['POST'])
def webhook():
	data = request.json
	notifications=data["notifications"]
	nodes_data = json.loads(open('js/nodes.js').read())
	for notif in notifications:
		#if str(notif["deviceId"]).replace(':','').upper() in [element["name"] for element in nodes_data["all_nodes"]]:
		for node in nodes_data["all_nodes"]:
			if str(notif["deviceId"]).replace(':','').upper()==node["name"]:
				node["x"]=notif["locationCoordinate"]["x"]
				node["y"]=notif["locationCoordinate"]["y"]
				with open('js/nodes.js', 'w') as jsonfile:
					json.dump(nodes_data,jsonfile,indent=4)
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


def creat_topology(status,tags):
	if status!='VLAN':
		with open('static/index.js', 'w') as outfile, open('index.js.template', 'r') as infile:
			#rooms_data = json.loads(open('js/rooms.js').read())
			#nodes_data = json.loads(open('js/nodes.js').read())
			infile_data=infile.read()
			infile_data=infile_data.replace("{nodes_replace}",(",".join(json.dumps(node) for node in tags)))
			outfile.write(infile_data)
			outfile.close()

if __name__ == "__main__":
	app.run(threaded=True)