# app.py

# Importing necessary libraries
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
import io
import base64
import plotly.express as px
import json
import plotly.utils
import plotly



# Initializing Flask application
app = Flask(__name__)

# Establishing MySQL connection
app.secret_key = "anakitiktokwimandidalamkolam"
userpass = "mysql+pymysql://root:@"
basedir = "127.0.0.1"
dbname = "/forest-v3"

app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class CutTrees(db.Model):
    __tablename__ = 'newforestnew'
    __table_args__ = (
        db.PrimaryKeyConstraint('Block_X', 'Block_Y', 'Tree_Number'),
    )
    Block_X = db.Column(db.Integer, nullable=False)
    Block_Y = db.Column(db.Integer, nullable=False)
    Coordinate_X = db.Column(db.Integer)
    Coordinate_Y = db.Column(db.Integer)
    Tree_Number = db.Column(db.String(9), nullable=False)
    SPECODE = db.Column(db.String(14))
    SPECIES_GROUP = db.Column(db.Integer, name='SPECIES-GROUP')
    Diameter_cm = db.Column(db.Numeric(5, 2), name='Diameter (cm)')
    Diameter_Class = db.Column(db.Integer, name='Diameter Class')
    Height_m = db.Column(db.Numeric(4, 2), name='Height (m)')
    Volume_m3 = db.Column(db.Numeric(7, 5), name='Volume (m^3)')
    Status = db.Column(db.String(4))
    Production = db.Column(db.Numeric(8, 2))
    Cut_Volume_m3 = db.Column(db.String(7), name='Cut Volume (m^3)')
    Cutting_Angle = db.Column(db.Numeric(4, 1), name='Cutting Angle')
    Damage_Crown = db.Column(db.String(6), name='Damage Crown')
    Damage_Stem = db.Column(db.String(8), name='Damage Stem')
    Diameter_30 = db.Column(db.Numeric(5, 2), name='Diameter_30')
    Production_30 = db.Column(db.Numeric(10, 5), name='Production_30')
    Diameter_after_30_years = db.Column(db.Numeric(5, 2), name='Diameter after 30 years')
    Volume_after_30_years = db.Column(db.Numeric(8, 2), name='Volume after 30 years')

    def __init__(self, Block_X, Block_Y, Coordinate_X, Coordinate_Y, Tree_Number, SPECODE, SPECIES_GROUP, Diameter_cm, Diameter_Class, Height_m, Volume_m3, Status, Production, Cut_Volume_m3, Cutting_Angle, Damage_Crown, Damage_Stem, Diameter_30, Production_30, Diameter_after_30_years, Volume_after_30_years):
        self.Block_X = Block_X
        self.Block_Y = Block_Y
        self.Coordinate_X = Coordinate_X
        self.Coordinate_Y = Coordinate_Y
        self.Tree_Number = Tree_Number
        self.SPECODE = SPECODE
        self.SPECIES_GROUP = SPECIES_GROUP
        self.Diameter_cm = Diameter_cm
        self.Diameter_Class = Diameter_Class
        self.Height_m = Height_m
        self.Volume_m3 = Volume_m3
        self.Status = Status
        self.Production = Production
        self.Cut_Volume_m3 = Cut_Volume_m3
        self.Cutting_Angle = Cutting_Angle
        self.Damage_Crown = Damage_Crown
        self.Damage_Stem = Damage_Stem
        self.Diameter_30 = Diameter_30
        self.Production_30 = Production_30
        self.Diameter_after_30_years = Diameter_after_30_years
        self.Volume_after_30_years = Volume_after_30_years
    
    
class StandTable(db.Model):
    __tablename__ = 'stand_table_2'
    Species_Group = db.Column('Species Group', db.Integer, primary_key=True)
    Total_Volume_m3 = db.Column('Total Volume (m^3)', db.Float(precision=8))
    Total_Number_of_Trees = db.Column('Total Number of Trees', db.Integer)
    Diameter_5_15_cm = db.Column('5-15 cm', db.Integer)
    Diameter_15_30_cm = db.Column('15-30 cm', db.Integer)
    Diameter_30_45_cm = db.Column('30-45 cm', db.Integer)
    Diameter_45_60_cm = db.Column('45-60 cm', db.Integer)
    Diameter_60_250_cm = db.Column('60-250 cm', db.Integer)

    def __init__(self, Species_Group, Total_Volume_m3, Total_Number_of_Trees, Diameter_5_15_cm, Diameter_15_30_cm, Diameter_30_45_cm, Diameter_45_60_cm, Diameter_60_250_cm):
        self.Species_Group = Species_Group
        self.Total_Volume_m3 = Total_Volume_m3
        self.Total_Number_of_Trees = Total_Number_of_Trees
        self.Diameter_5_15_cm = Diameter_5_15_cm
        self.Diameter_15_30_cm = Diameter_15_30_cm
        self.Diameter_30_45_cm = Diameter_30_45_cm
        self.Diameter_45_60_cm = Diameter_45_60_cm
        self.Diameter_60_250_cm = Diameter_60_250_cm

class StandTable30(db.Model):
    __tablename__ = 'stand_table_30'
    Species_Group = db.Column('Species Group', db.Integer, primary_key=True)
    Total_Volume_m3 = db.Column('Total Volume (m^3)', db.Float(precision=8))
    Total_Production = db.Column('Total Production', db.Float(precision=8))
    # Total_Damage_Crown_m = db.Column('Total Damage Crown (m)', db.Float(precision=8))
    Total_Damage_Stem = db.Column('Total Damage Stem', db.Float(precision=8))
    Total_Diameter_after_30_years = db.Column('Total Diameter after 30 years', db.Float(precision=8))
    Total_Production_after_30_years = db.Column('Total Production after 30 years', db.Float(precision=8))

    def __init__(self, Species_Group, Total_Volume_m3, Total_Production, Total_Damage_Crown_m, Total_Damage_Stem, Total_Diameter_after_30_years, Total_Production_after_30_years):
        self.Species_Group = Species_Group
        self.Total_Volume_m3 = Total_Volume_m3
        self.Total_Production = Total_Production
        # self.Total_Damage_Crown_m = Total_Damage_Crown_m
        self.Total_Damage_Stem = Total_Damage_Stem
        self.Total_Diameter_after_30_years = Total_Diameter_after_30_years
        self.Total_Production_after_30_years = Total_Production_after_30_years

class SpeciesGroup(db.Model):
    __tablename__ = 'species_group'
    SPRGROUP = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(20))

@app.route('/debug')
def debug():
    # # Query all data
    # cut_trees = CutTrees.query.all()
    # return render_template('debug.html', cut_trees=cut_trees)

    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of items per page

    pagination = CutTrees.query.paginate(page=page, per_page=per_page)

    cut_trees = pagination.items

    return render_template('debug.html', cut_trees=cut_trees, pagination=pagination)


# Setup route to every html page
@app.route('/')
def index():
    # Get the page number from the query parameters (default to 1 if not provided)
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of items per page

    pagination = CutTrees.query.paginate(page=page, per_page=per_page)

    cut_trees = pagination.items

    # Debugging: Print the entire data row
    # for tree in cut_trees:
    #     print(vars(tree))  # Print all attributes of the SQLAlchemy model

    return render_template('index.html', cut_trees=cut_trees, pagination=pagination)

@app.route('/input', methods=['POST', 'GET'])
def input_tree():
    if request.method == 'POST':
        # Getting form data from the request
        block_x = request.form.get('block_x', type=int)
        block_y = request.form.get('block_y', type=int)
        coordinate_x = request.form.get('coordinate_x', type=int)
        coordinate_y = request.form.get('coordinate_y', type=int)
        tree_number = request.form.get('tree_number')
        specode = request.form.get('specode')
        species_group = request.form.get('species_group', type=int)
        diameter_cm = request.form.get('diameter_cm', type=float)
        diameter_class = request.form.get('diameter_class', type=int)
        height_m = request.form.get('height_m', type=float)
        volume_m3 = request.form.get('volume_m3', type=float)
        status = request.form.get('status')
        production = request.form.get('production', type=float)
        cut_volume_m3 = request.form.get('cut_volume_m3')
        cutting_angle = request.form.get('cutting_angle', type=float)
        damage_crown = request.form.get('damage_crown')
        damage_stem = request.form.get('damage_stem')
        diameter_30 = request.form.get('diameter_30', type=float)
        production_30 = request.form.get('production_30', type=float)
        diameter_after_30_years = request.form.get('diameter_after_30_years', type=float)
        volume_after_30_years = request.form.get('volume_after_30_years', type=float)

        # Create a new CutTrees instance with the form data
        add_data = CutTrees(
            Block_X=block_x,
            Block_Y=block_y,
            Coordinate_X=coordinate_x,
            Coordinate_Y=coordinate_y,
            Tree_Number=tree_number,
            SPECODE=specode,
            SPECIES_GROUP=species_group,
            Diameter_cm=diameter_cm,
            Diameter_Class=diameter_class,
            Height_m=height_m,
            Volume_m3=volume_m3,
            Status=status,
            Production=production,
            Cut_Volume_m3=cut_volume_m3,
            Cutting_Angle=cutting_angle,
            Damage_Crown=damage_crown,
            Damage_Stem=damage_stem,
            Diameter_30=diameter_30,
            Production_30=production_30,
            Diameter_after_30_years=diameter_after_30_years,
            Volume_after_30_years=volume_after_30_years
        )

        # Add the new CutTrees instance to the session and commit it to the database
        db.session.add(add_data)
        db.session.commit()

        # Redirect to the index page after successful form submission
        return redirect(url_for('index'))
    
    # Render the input form if the request method is GET
    return render_template('input_forest.html')

@app.route('/stand_table')
def stand_table():
    all_stand_data = StandTable.query.all()
    return render_template('stand_table.html', stand_data=all_stand_data)

@app.route('/stand_table_30')
def stand_table_30():
    all_stand_data_30 = StandTable30.query.all()
    return render_template('stand_table_30.html', stand_table_30=all_stand_data_30)

@app.route('/species_group')
def species_group():
    species_group = SpeciesGroup.query.all()
    return render_template('species_group.html', species=species_group)


@app.route('/volume_calculation', methods=['GET', 'POST'])
def volume():
    volume_result = None
    if request.method == 'POST':
        try:
            diameter = float(request.form['diameter'])
            height = float(request.form['height'])
            volume_result = 3.142 * round((diameter / 200) ** 2 * (height * 0.50), 2) / 1000000  # Calculate volume in cubic meters
        except ValueError:
            flash('Please enter valid numerical values for diameter and height.', 'danger')

    return render_template('volume.html', volume_result=volume_result)


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/tree_distribution')
def tree_distribution():
    # Retrieve tree data
    all_trees = CutTrees.query.limit(500).all()

    # Separate cut and kept trees based on status
    cut_trees = [(tree.Coordinate_X, tree.Coordinate_Y, tree.Tree_Number, tree.Status, tree.Damage_Crown, tree.Damage_Stem) for tree in all_trees if tree.Status == 'Cut']
    kept_trees = [(tree.Coordinate_X, tree.Coordinate_Y, tree.Tree_Number, tree.Status, tree.Damage_Crown, tree.Damage_Stem) for tree in all_trees if tree.Status == 'Keep']

    # Prepare data for Plotly
    cut_x, cut_y, cut_tree_number, cut_status, cut_damage_crown, cut_damage_stem = zip(*cut_trees) if cut_trees else ([],[], [], [], [], [])
    keep_x, keep_y, kept_tree_number, keep_status, keep_damage_crown, keep_damage_stem = zip(*kept_trees) if kept_trees else ([],[], [], [], [], [])

    # Create a Plotly scatter plot
    fig = px.scatter(
        x=cut_x + keep_x,
        y=cut_y + keep_y,
        color=cut_status + keep_status,
        color_discrete_map={'Keep': 'green', 'Cut': 'red'},  # Set colors for 'Keep' and 'Cut'
        labels={'x': 'X Coordinate', 'y': 'Y Coordinate', 'color': 'Status'},
        title='Tree Distribution',
        hover_name=None,  # Exclude tree names from hover
        hover_data={'Tree Number':  cut_tree_number + kept_tree_number, 'Damage': cut_damage_stem + keep_damage_stem}
    )

    fig.update_traces(marker=dict(size=8))
    fig.update_layout(legend_title_text='Tree Status')

    # Convert Plotly figure to JSON
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Render the HTML page with the Plotly graph
    return render_template('tree_distribution.html', graph_json=graph_json)




@app.route('/sustainable')
def sustainable():
    # Fetch all StandTable30 data from the database
    all_stand_data_30 = StandTable30.query.all()

    # Prepare data for Plotly graphs
    x_values = [stand.Species_Group for stand in all_stand_data_30]
    initial_production_values = [stand.Total_Production for stand in all_stand_data_30]
    initial_volume_values = [stand.Total_Volume_m3 for stand in all_stand_data_30]
    thirty_years_production_values = [stand.Total_Production_after_30_years for stand in all_stand_data_30]
    thirty_years_diameter_values = [stand.Total_Diameter_after_30_years for stand in all_stand_data_30]

    # Pass the fetched data and graph data to the template for rendering
    return render_template('sustainable.html', 
                           stand_data_30=all_stand_data_30, 
                           x_values=x_values, 
                           initial_production_values=initial_production_values, 
                           initial_volume_values=initial_volume_values,
                           thirty_years_production_values=thirty_years_production_values,
                           thirty_years_diameter_values=thirty_years_diameter_values)



if __name__ == '__main__':
    # Running the Flask application
    # app.run(host='127.0.0.1')
    app.run(debug=True)
