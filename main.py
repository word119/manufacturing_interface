from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

app = Flask(__name__)
# Enable CORS for REST API endpoints
CORS(app, resources={r"/api/*": {"origins": "*"}})

# CREATE DATABASE


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///manufacturing.db"
# Create the extension
db = SQLAlchemy(model_class=Base)
# initialise the app with the extension
db.init_app(app)


# CREATE TABLES
class Contact(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    Description: Mapped[str] = mapped_column(String(250), nullable=False)
    Diameter: Mapped[str] = mapped_column(String(50), nullable=False)
    Insertdepth: Mapped[str] = mapped_column(String(50), nullable=False)
    Name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    ZF_ContNumb: Mapped[str] = mapped_column(String(50), nullable=False)


class Wire(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    cross_section: Mapped[str] = mapped_column(String(100), nullable=False)
    isolation_diameter: Mapped[str] = mapped_column(String(50), nullable=False)
    wire_diameter: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[str] = mapped_column(String(50), nullable=False)


class Process(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    crimping_depth_d: Mapped[str] = mapped_column(String(50), nullable=False)
    crimping_depth_offset_d: Mapped[str] = mapped_column(String(50), nullable=False)
    holding_value_delta_d: Mapped[str] = mapped_column(String(50), nullable=False)
    insertion_depth_delta_d: Mapped[str] = mapped_column(String(50), nullable=False)
    sf_performance_d: Mapped[str] = mapped_column(String(50), nullable=False)
    sf_frequence_d: Mapped[str] = mapped_column(String(50), nullable=False)
    extendable_feeder_tuble_s: Mapped[str] = mapped_column(String(50), nullable=False)
    loading_holding_jaws_s: Mapped[str] = mapped_column(String(50), nullable=False)
    catact_monitoring_s: Mapped[str] = mapped_column(String(50), nullable=False)
    wayback_d: Mapped[str] = mapped_column(String(50), nullable=False)
    stripping_position: Mapped[str] = mapped_column(String(50), nullable=False)
    stripping_function: Mapped[str] = mapped_column(String(50), nullable=False)
    crimping_position_monitoring: Mapped[str] = mapped_column(String(50), nullable=False)


class Recipe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    contact_id: Mapped[int] = mapped_column(Integer, ForeignKey('contact.id', ondelete='CASCADE'), nullable=False)
    wire_id: Mapped[int] = mapped_column(Integer, ForeignKey('wire.id', ondelete='CASCADE'), nullable=False)
    process_id: Mapped[int] = mapped_column(Integer, ForeignKey('process.id', ondelete='CASCADE'), nullable=False)
    
    contact = relationship("Contact", backref="recipes")
    wire = relationship("Wire", backref="recipes")
    process = relationship("Process", backref="recipes")


class Job(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    created_at: Mapped[str] = mapped_column(String(100), nullable=False)


class Setup(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active")


class Command(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")


# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()


# Custom error handlers for JSON responses
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400


@app.route('/')
def home():
    # READ ALL RECORDS
    contacts = db.session.execute(db.select(Contact).order_by(Contact.Name)).scalars().all()
    wires = db.session.execute(db.select(Wire).order_by(Wire.name)).scalars().all()
    processes = db.session.execute(db.select(Process).order_by(Process.name)).scalars().all()
    recipes = db.session.execute(db.select(Recipe).order_by(Recipe.description)).scalars().all()
    jobs = db.session.execute(db.select(Job).order_by(Job.id)).scalars().all()
    setups = db.session.execute(db.select(Setup).order_by(Setup.id)).scalars().all()
    commands = db.session.execute(db.select(Command).order_by(Command.id)).scalars().all()
    
    return render_template("index.html", 
                         contacts=contacts, 
                         wires=wires, 
                         processes=processes, 
                         recipes=recipes,
                         jobs=jobs,
                         setups=setups,
                         commands=commands)


@app.route('/api/demo')
def demo():
    """Demonstration endpoint showing current data"""
    try:
        # READ ALL RECORDS
        contacts = db.session.execute(db.select(Contact).order_by(Contact.Name)).scalars().all()
        wires = db.session.execute(db.select(Wire).order_by(Wire.name)).scalars().all()
        processes = db.session.execute(db.select(Process).order_by(Process.name)).scalars().all()
        recipes = db.session.execute(db.select(Recipe).order_by(Recipe.description)).scalars().all()
        jobs = db.session.execute(db.select(Job).order_by(Job.id)).scalars().all()
        setups = db.session.execute(db.select(Setup).order_by(Setup.id)).scalars().all()
        commands = db.session.execute(db.select(Command).order_by(Command.id)).scalars().all()
        
        demo_data = {
            "server_info": {
                "name": "Manufacturing REST API Server",
                "version": "1.0",
                "description": "Demonstration server for manufacturing data management",
                "timestamp": datetime.now(pytz.timezone("Europe/Berlin")).isoformat()
            },
            "database_stats": {
                "contacts": len(contacts),
                "wires": len(wires),
                "processes": len(processes),
                "recipes": len(recipes),
                "jobs": len(jobs),
                "setups": len(setups),
                "commands": len(commands)
            },
            "sample_data": {
                "contacts": [model_to_dict(contact) for contact in contacts[:3]],  # Show first 3
                "wires": [model_to_dict(wire) for wire in wires[:3]],
                "processes": [model_to_dict(process) for process in processes[:3]],
                "recipes": [recipe_to_dict(recipe) for recipe in recipes[:3]],
                "jobs": [model_to_dict(job) for job in jobs[:3]],
                "setups": [model_to_dict(setup) for setup in setups[:3]],
                "commands": [model_to_dict(command) for command in commands[:3]]
            },
            "api_endpoints": {
                "rest_api_base": "/api/v1",
                "documentation": "/api/v1/docs",
                "available_resources": [
                    "contacts", "wires", "processes", "recipes", 
                    "jobs", "setups", "commands"
                ],
                "device_control": "/api/v1/device/commands"
            },
            "usage_examples": {
                "get_all_contacts": "GET /api/v1/contacts",
                "get_contact_by_id": "GET /api/v1/contacts/1",
                "create_contact": "POST /api/v1/contacts",
                "update_contact": "PUT /api/v1/contacts/1",
                "delete_contact": "DELETE /api/v1/contacts/1",
                "start_recipe": "POST /api/v1/device/commands"
            }
        }
        
        return jsonify(demo_data), 200
    except Exception as e:
        return jsonify({"error": f"Failed to generate demo data: {str(e)}"}), 500


@app.route("/add_contact", methods=["GET", "POST"])
def add_contact():
    if request.method == "POST":
        contact_data = {
            "Description": request.form["description"],
            "Diameter": request.form["diameter"],
            "Insertdepth": request.form["insertdepth"],
            "Name": request.form["name"],
            "ZF_ContNumb": request.form["zf_contnumb"]
        }
        new_contact = Contact(**contact_data)
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add_contact.html")


@app.route("/add_wire", methods=["GET", "POST"])
def add_wire():
    if request.method == "POST":
        wire_data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "cross_section": request.form["cross_section"],
            "isolation_diameter": request.form["isolation_diameter"],
            "wire_diameter": request.form["wire_diameter"],
            "color": request.form["color"]
        }
        new_wire = Wire(**wire_data)
        db.session.add(new_wire)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add_wire.html")


@app.route("/add_process", methods=["GET", "POST"])
def add_process():
    if request.method == "POST":
        process_data = {
            "name": request.form["name"],
            "crimping_depth_d": request.form["crimping_depth_d"],
            "crimping_depth_offset_d": request.form["crimping_depth_offset_d"],
            "holding_value_delta_d": request.form["holding_value_delta_d"],
            "insertion_depth_delta_d": request.form["insertion_depth_delta_d"],
            "sf_performance_d": request.form["sf_performance_d"],
            "sf_frequence_d": request.form["sf_frequence_d"],
            "extendable_feeder_tuble_s": request.form["extendable_feeder_tuble_s"],
            "loading_holding_jaws_s": request.form["loading_holding_jaws_s"],
            "catact_monitoring_s": request.form["catact_monitoring_s"],
            "wayback_d": request.form["wayback_d"],
            "stripping_position": request.form["stripping_position"],
            "stripping_function": request.form["stripping_function"],
            "crimping_position_monitoring": request.form["crimping_position_monitoring"]
        }
        new_process = Process(**process_data)
        db.session.add(new_process)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add_process.html")


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe_data = {
            "description": request.form["description"],
            "contact_id": request.form["contact_id"],
            "wire_id": request.form["wire_id"],
            "process_id": request.form["process_id"]
        }
        new_recipe = Recipe(**recipe_data)
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('home'))
    
    contacts = db.session.execute(db.select(Contact).order_by(Contact.Name)).scalars().all()
    wires = db.session.execute(db.select(Wire).order_by(Wire.name)).scalars().all()
    processes = db.session.execute(db.select(Process).order_by(Process.name)).scalars().all()
    
    return render_template("add_recipe.html", contacts=contacts, wires=wires, processes=processes)


@app.route("/edit_contact", methods=["GET", "POST"])
def edit_contact():
    if request.method == "POST":
        contact_id = request.form["id"]
        contact_to_update = db.get_or_404(Contact, contact_id)
        contact_data = {
            "Description": request.form["description"],
            "Diameter": request.form["diameter"],
            "Insertdepth": request.form["insertdepth"],
            "Name": request.form["name"],
            "ZF_ContNumb": request.form["zf_contnumb"]
        }
        for key, value in contact_data.items():
            setattr(contact_to_update, key, value)
        db.session.commit()
        return redirect(url_for('home'))
    contact_id = request.args.get('id')
    contact_selected = db.get_or_404(Contact, contact_id)
    return render_template("edit_contact.html", contact=contact_selected)


@app.route("/edit_wire", methods=["GET", "POST"])
def edit_wire():
    if request.method == "POST":
        wire_id = request.form["id"]
        wire_to_update = db.get_or_404(Wire, wire_id)
        wire_data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "cross_section": request.form["cross_section"],
            "isolation_diameter": request.form["isolation_diameter"],
            "wire_diameter": request.form["wire_diameter"],
            "color": request.form["color"]
        }
        for key, value in wire_data.items():
            setattr(wire_to_update, key, value)
        db.session.commit()
        return redirect(url_for('home'))
    wire_id = request.args.get('id')
    wire_selected = db.get_or_404(Wire, wire_id)
    return render_template("edit_wire.html", wire=wire_selected)


@app.route("/edit_process", methods=["GET", "POST"])
def edit_process():
    if request.method == "POST":
        process_id = request.form["id"]
        process_to_update = db.get_or_404(Process, process_id)
        process_data = {
            "name": request.form["name"],
            "crimping_depth_d": request.form["crimping_depth_d"],
            "crimping_depth_offset_d": request.form["crimping_depth_offset_d"],
            "holding_value_delta_d": request.form["holding_value_delta_d"],
            "insertion_depth_delta_d": request.form["insertion_depth_delta_d"],
            "sf_performance_d": request.form["sf_performance_d"],
            "sf_frequence_d": request.form["sf_frequence_d"],
            "extendable_feeder_tuble_s": request.form["extendable_feeder_tuble_s"],
            "loading_holding_jaws_s": request.form["loading_holding_jaws_s"],
            "catact_monitoring_s": request.form["catact_monitoring_s"],
            "wayback_d": request.form["wayback_d"],
            "stripping_position": request.form["stripping_position"],
            "stripping_function": request.form["stripping_function"],
            "crimping_position_monitoring": request.form["crimping_position_monitoring"]
        }
        for key, value in process_data.items():
            setattr(process_to_update, key, value)
        db.session.commit()
        return redirect(url_for('home'))
    process_id = request.args.get('id')
    process_selected = db.get_or_404(Process, process_id)
    return render_template("edit_process.html", process=process_selected)


@app.route("/edit_recipe", methods=["GET", "POST"])
def edit_recipe():
    if request.method == "POST":
        recipe_id = request.form["id"]
        recipe_to_update = db.get_or_404(Recipe, recipe_id)
        recipe_data = {
            "description": request.form["description"],
            "contact_id": request.form["contact_id"],
            "wire_id": request.form["wire_id"],
            "process_id": request.form["process_id"]
        }
        for key, value in recipe_data.items():
            setattr(recipe_to_update, key, value)
        db.session.commit()
        return redirect(url_for('home'))
    
    recipe_id = request.args.get('id')
    recipe_selected = db.get_or_404(Recipe, recipe_id)
    contacts = db.session.execute(db.select(Contact).order_by(Contact.Name)).scalars().all()
    wires = db.session.execute(db.select(Wire).order_by(Wire.name)).scalars().all()
    processes = db.session.execute(db.select(Process).order_by(Process.name)).scalars().all()
    
    return render_template("edit_recipe.html", recipe=recipe_selected, contacts=contacts, wires=wires, processes=processes)


@app.route("/delete_contact", methods=["DELETE"])
def delete_contact():
    try:
        contact_id = request.args.get('id')
        if not contact_id:
            return jsonify({"error": "Contact ID is required"}), 400
        
        contact_to_delete = db.session.get(Contact, contact_id)
        if not contact_to_delete:
            return jsonify({"error": "Contact not found"}), 404
        
        # Delete related recipes first
        related_recipes = db.session.execute(db.select(Recipe).where(Recipe.contact_id == contact_id)).scalars().all()
        for recipe in related_recipes:
            db.session.delete(recipe)
        
        # Now delete the contact
        db.session.delete(contact_to_delete)
        db.session.commit()
        return jsonify({"message": "Contact deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete contact: {str(e)}"}), 500


@app.route("/delete_wire", methods=["DELETE"])
def delete_wire():
    try:
        wire_id = request.args.get('id')
        if not wire_id:
            return jsonify({"error": "Wire ID is required"}), 400
        
        wire_to_delete = db.session.get(Wire, wire_id)
        if not wire_to_delete:
            return jsonify({"error": "Wire not found"}), 404
        
        # Delete related recipes first
        related_recipes = db.session.execute(db.select(Recipe).where(Recipe.wire_id == wire_id)).scalars().all()
        for recipe in related_recipes:
            db.session.delete(recipe)
        
        # Now delete the wire
        db.session.delete(wire_to_delete)
        db.session.commit()
        return jsonify({"message": "Wire deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete wire: {str(e)}"}), 500


@app.route("/delete_process", methods=["DELETE"])
def delete_process():
    try:
        process_id = request.args.get('id')
        if not process_id:
            return jsonify({"error": "Process ID is required"}), 400
        
        process_to_delete = db.session.get(Process, process_id)
        if not process_to_delete:
            return jsonify({"error": "Process not found"}), 404
        
        # Delete related recipes first
        related_recipes = db.session.execute(db.select(Recipe).where(Recipe.process_id == process_id)).scalars().all()
        for recipe in related_recipes:
            db.session.delete(recipe)
        
        # Now delete the process
        db.session.delete(process_to_delete)
        db.session.commit()
        return jsonify({"message": "Process deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete process: {str(e)}"}), 500


@app.route("/delete_recipe", methods=["DELETE"])
def delete_recipe():
    try:
        recipe_id = request.args.get('id')
        if not recipe_id:
            return jsonify({"error": "Recipe ID is required"}), 400
        
        recipe_to_delete = db.session.get(Recipe, recipe_id)
        if not recipe_to_delete:
            return jsonify({"error": "Recipe not found"}), 404
        
        db.session.delete(recipe_to_delete)
        db.session.commit()
        return jsonify({"message": "Recipe deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete recipe: {str(e)}"}), 500


@app.route("/delete_job", methods=["DELETE"])
def delete_job():
    try:
        job_id = request.args.get('id')
        if not job_id:
            return jsonify({"error": "Job ID is required"}), 400
        
        job_to_delete = db.session.get(Job, job_id)
        if not job_to_delete:
            return jsonify({"error": "Job not found"}), 404
        
        db.session.delete(job_to_delete)
        db.session.commit()
        return jsonify({"message": "Job deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete job: {str(e)}"}), 500


@app.route("/delete_setup", methods=["DELETE"])
def delete_setup():
    try:
        setup_id = request.args.get('id')
        if not setup_id:
            return jsonify({"error": "Setup ID is required"}), 400
        
        setup_to_delete = db.session.get(Setup, setup_id)
        if not setup_to_delete:
            return jsonify({"error": "Setup not found"}), 404
        
        db.session.delete(setup_to_delete)
        db.session.commit()
        return jsonify({"message": "Setup deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete setup: {str(e)}"}), 500


@app.route("/delete_command", methods=["DELETE"])
def delete_command():
    try:
        command_id = request.args.get('id')
        if not command_id:
            return jsonify({"error": "Command ID is required"}), 400
        
        command_to_delete = db.session.get(Command, command_id)
        if not command_to_delete:
            return jsonify({"error": "Command not found"}), 404
        
        db.session.delete(command_to_delete)
        db.session.commit()
        return jsonify({"message": "Command deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete command: {str(e)}"}), 500


# ============================================================================
# REST API ENDPOINTS FOR CUSTOMER INTEGRATION
# ============================================================================

# Helper function to convert SQLAlchemy objects to dictionaries
def model_to_dict(obj):
    if obj is None:
        return None
    result = {}
    for column in obj.__table__.columns:
        result[column.name] = getattr(obj, column.name)
    return result

# Helper function to convert Recipe with relationships to dictionary
def recipe_to_dict(recipe):
    if recipe is None:
        return None
    result = {
        'id': recipe.id,
        'description': recipe.description,
        'contact_id': recipe.contact_id,
        'wire_id': recipe.wire_id,
        'process_id': recipe.process_id,
        'contact': model_to_dict(recipe.contact),
        'wire': model_to_dict(recipe.wire),
        'process': model_to_dict(recipe.process)
    }
    return result

# CONTACTS API
@app.route('/api/v1/contacts', methods=['GET'])
def api_get_contacts():
    """Get all contacts"""
    try:
        contacts = db.session.execute(db.select(Contact).order_by(Contact.id)).scalars().all()
        return jsonify([model_to_dict(contact) for contact in contacts]), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch contacts: {str(e)}"}), 500

@app.route('/api/v1/contacts/<int:contact_id>', methods=['GET'])
def api_get_contact(contact_id):
    """Get a specific contact by ID"""
    try:
        contact = db.session.get(Contact, contact_id)
        if not contact:
            return jsonify({"error": "Contact not found"}), 404
        return jsonify(model_to_dict(contact)), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch contact: {str(e)}"}), 500

@app.route('/api/v1/contacts', methods=['POST'])
def api_create_contact():
    """Create a new contact"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.json
        required_fields = ['Description', 'Diameter', 'Insertdepth', 'Name', 'ZF_ContNumb']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        new_contact = Contact(**data)
        db.session.add(new_contact)
        db.session.commit()
        
        return jsonify(model_to_dict(new_contact)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create contact: {str(e)}"}), 500

@app.route('/api/v1/contacts/<int:contact_id>', methods=['PUT'])
def api_update_contact(contact_id):
    """Update a contact"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        contact = db.session.get(Contact, contact_id)
        if not contact:
            return jsonify({"error": "Contact not found"}), 404
        
        data = request.json
        for key, value in data.items():
            if hasattr(contact, key):
                setattr(contact, key, value)
        
        db.session.commit()
        return jsonify(model_to_dict(contact)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update contact: {str(e)}"}), 500

@app.route('/api/v1/contacts/<int:contact_id>', methods=['DELETE'])
def api_delete_contact(contact_id):
    """Delete a contact"""
    try:
        contact = db.session.get(Contact, contact_id)
        if not contact:
            return jsonify({"error": "Contact not found"}), 404
        
        # Delete related recipes first
        related_recipes = db.session.execute(db.select(Recipe).where(Recipe.contact_id == contact_id)).scalars().all()
        for recipe in related_recipes:
            db.session.delete(recipe)
        
        db.session.delete(contact)
        db.session.commit()
        return jsonify({"message": "Contact deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete contact: {str(e)}"}), 500

# WIRES API
@app.route('/api/v1/wires', methods=['GET'])
def api_get_wires():
    """Get all wires"""
    try:
        wires = db.session.execute(db.select(Wire).order_by(Wire.id)).scalars().all()
        return jsonify([model_to_dict(wire) for wire in wires]), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch wires: {str(e)}"}), 500

@app.route('/api/v1/wires/<int:wire_id>', methods=['GET'])
def api_get_wire(wire_id):
    """Get a specific wire by ID"""
    try:
        wire = db.session.get(Wire, wire_id)
        if not wire:
            return jsonify({"error": "Wire not found"}), 404
        return jsonify(model_to_dict(wire)), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch wire: {str(e)}"}), 500

@app.route('/api/v1/wires', methods=['POST'])
def api_create_wire():
    """Create a new wire"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.json
        required_fields = ['name', 'description', 'cross_section', 'isolation_diameter', 'wire_diameter', 'color']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        new_wire = Wire(**data)
        db.session.add(new_wire)
        db.session.commit()
        
        return jsonify(model_to_dict(new_wire)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create wire: {str(e)}"}), 500

@app.route('/api/v1/wires/<int:wire_id>', methods=['PUT'])
def api_update_wire(wire_id):
    """Update a wire"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        wire = db.session.get(Wire, wire_id)
        if not wire:
            return jsonify({"error": "Wire not found"}), 404
        
        data = request.json
        for key, value in data.items():
            if hasattr(wire, key):
                setattr(wire, key, value)
        
        db.session.commit()
        return jsonify(model_to_dict(wire)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update wire: {str(e)}"}), 500

@app.route('/api/v1/wires/<int:wire_id>', methods=['DELETE'])
def api_delete_wire(wire_id):
    """Delete a wire"""
    try:
        wire = db.session.get(Wire, wire_id)
        if not wire:
            return jsonify({"error": "Wire not found"}), 404
        
        # Delete related recipes first
        related_recipes = db.session.execute(db.select(Recipe).where(Recipe.wire_id == wire_id)).scalars().all()
        for recipe in related_recipes:
            db.session.delete(recipe)
        
        db.session.delete(wire)
        db.session.commit()
        return jsonify({"message": "Wire deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete wire: {str(e)}"}), 500

# PROCESSES API
@app.route('/api/v1/processes', methods=['GET'])
def api_get_processes():
    """Get all processes"""
    try:
        processes = db.session.execute(db.select(Process).order_by(Process.id)).scalars().all()
        return jsonify([model_to_dict(process) for process in processes]), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch processes: {str(e)}"}), 500

@app.route('/api/v1/processes/<int:process_id>', methods=['GET'])
def api_get_process(process_id):
    """Get a specific process by ID"""
    try:
        process = db.session.get(Process, process_id)
        if not process:
            return jsonify({"error": "Process not found"}), 404
        return jsonify(model_to_dict(process)), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch process: {str(e)}"}), 500

@app.route('/api/v1/processes', methods=['POST'])
def api_create_process():
    """Create a new process"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.json
        required_fields = ['name', 'crimping_depth_d', 'crimping_depth_offset_d', 'holding_value_delta_d', 
                          'insertion_depth_delta_d', 'sf_performance_d', 'sf_frequence_d', 
                          'extendable_feeder_tuble_s', 'loading_holding_jaws_s', 'catact_monitoring_s',
                          'wayback_d', 'stripping_position', 'stripping_function', 'crimping_position_monitoring']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        new_process = Process(**data)
        db.session.add(new_process)
        db.session.commit()
        
        return jsonify(model_to_dict(new_process)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create process: {str(e)}"}), 500

@app.route('/api/v1/processes/<int:process_id>', methods=['PUT'])
def api_update_process(process_id):
    """Update a process"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        process = db.session.get(Process, process_id)
        if not process:
            return jsonify({"error": "Process not found"}), 404
        
        data = request.json
        for key, value in data.items():
            if hasattr(process, key):
                setattr(process, key, value)
        
        db.session.commit()
        return jsonify(model_to_dict(process)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update process: {str(e)}"}), 500

@app.route('/api/v1/processes/<int:process_id>', methods=['DELETE'])
def api_delete_process(process_id):
    """Delete a process"""
    try:
        process = db.session.get(Process, process_id)
        if not process:
            return jsonify({"error": "Process not found"}), 404
        
        # Delete related recipes first
        related_recipes = db.session.execute(db.select(Recipe).where(Recipe.process_id == process_id)).scalars().all()
        for recipe in related_recipes:
            db.session.delete(recipe)
        
        db.session.delete(process)
        db.session.commit()
        return jsonify({"message": "Process deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete process: {str(e)}"}), 500

# RECIPES API
@app.route('/api/v1/recipes', methods=['GET'])
def api_get_recipes():
    """Get all recipes with full details"""
    try:
        recipes = db.session.execute(db.select(Recipe).order_by(Recipe.id)).scalars().all()
        return jsonify([recipe_to_dict(recipe) for recipe in recipes]), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch recipes: {str(e)}"}), 500

@app.route('/api/v1/recipes/<int:recipe_id>', methods=['GET'])
def api_get_recipe(recipe_id):
    """Get a specific recipe by ID with full details"""
    try:
        recipe = db.session.get(Recipe, recipe_id)
        if not recipe:
            return jsonify({"error": "Recipe not found"}), 404
        return jsonify(recipe_to_dict(recipe)), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch recipe: {str(e)}"}), 500

@app.route('/api/v1/recipes', methods=['POST'])
def api_create_recipe():
    """Create a new recipe"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.json
        required_fields = ['description', 'contact_id', 'wire_id', 'process_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate that referenced entities exist
        contact = db.session.get(Contact, data['contact_id'])
        wire = db.session.get(Wire, data['wire_id'])
        process = db.session.get(Process, data['process_id'])
        
        if not contact:
            return jsonify({"error": "Referenced contact not found"}), 400
        if not wire:
            return jsonify({"error": "Referenced wire not found"}), 400
        if not process:
            return jsonify({"error": "Referenced process not found"}), 400
        
        new_recipe = Recipe(**data)
        db.session.add(new_recipe)
        db.session.commit()
        
        return jsonify(recipe_to_dict(new_recipe)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create recipe: {str(e)}"}), 500

@app.route('/api/v1/recipes/<int:recipe_id>', methods=['PUT'])
def api_update_recipe(recipe_id):
    """Update a recipe"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        recipe = db.session.get(Recipe, recipe_id)
        if not recipe:
            return jsonify({"error": "Recipe not found"}), 404
        
        data = request.json
        for key, value in data.items():
            if hasattr(recipe, key):
                setattr(recipe, key, value)
        
        db.session.commit()
        return jsonify(recipe_to_dict(recipe)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update recipe: {str(e)}"}), 500

@app.route('/api/v1/recipes/<int:recipe_id>', methods=['DELETE'])
def api_delete_recipe(recipe_id):
    """Delete a recipe"""
    try:
        recipe = db.session.get(Recipe, recipe_id)
        if not recipe:
            return jsonify({"error": "Recipe not found"}), 404
        
        db.session.delete(recipe)
        db.session.commit()
        return jsonify({"message": "Recipe deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete recipe: {str(e)}"}), 500

# JOBS API
@app.route('/api/v1/jobs', methods=['GET'])
def api_get_jobs():
    """Get all jobs"""
    try:
        jobs = db.session.execute(db.select(Job).order_by(Job.id)).scalars().all()
        return jsonify([model_to_dict(job) for job in jobs]), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch jobs: {str(e)}"}), 500

@app.route('/api/v1/jobs/<int:job_id>', methods=['GET'])
def api_get_job(job_id):
    """Get a specific job by ID"""
    try:
        job = db.session.get(Job, job_id)
        if not job:
            return jsonify({"error": "Job not found"}), 404
        return jsonify(model_to_dict(job)), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch job: {str(e)}"}), 500

@app.route('/api/v1/jobs', methods=['POST'])
def api_create_job():
    """Create a new job"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.json
        if 'name' not in data:
            return jsonify({"error": "Missing required field: name"}), 400
        
        # Set default values
        data['status'] = data.get('status', 'pending')
        data['created_at'] = data.get('created_at', datetime.now(pytz.timezone("Europe/Berlin")).isoformat())
        
        new_job = Job(**data)
        db.session.add(new_job)
        db.session.commit()
        
        return jsonify(model_to_dict(new_job)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create job: {str(e)}"}), 500

@app.route('/api/v1/jobs/<int:job_id>', methods=['PUT'])
def api_update_job(job_id):
    """Update a job"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        job = db.session.get(Job, job_id)
        if not job:
            return jsonify({"error": "Job not found"}), 404
        
        data = request.json
        for key, value in data.items():
            if hasattr(job, key):
                setattr(job, key, value)
        
        db.session.commit()
        return jsonify(model_to_dict(job)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update job: {str(e)}"}), 500

@app.route('/api/v1/jobs/<int:job_id>', methods=['DELETE'])
def api_delete_job(job_id):
    """Delete a job"""
    try:
        job = db.session.get(Job, job_id)
        if not job:
            return jsonify({"error": "Job not found"}), 404
        
        db.session.delete(job)
        db.session.commit()
        return jsonify({"message": "Job deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete job: {str(e)}"}), 500

# SETUPS API
@app.route('/api/v1/setups', methods=['GET'])
def api_get_setups():
    """Get all setups"""
    try:
        setups = db.session.execute(db.select(Setup).order_by(Setup.id)).scalars().all()
        return jsonify([model_to_dict(setup) for setup in setups]), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch setups: {str(e)}"}), 500

@app.route('/api/v1/setups/<int:setup_id>', methods=['GET'])
def api_get_setup(setup_id):
    """Get a specific setup by ID"""
    try:
        setup = db.session.get(Setup, setup_id)
        if not setup:
            return jsonify({"error": "Setup not found"}), 404
        return jsonify(model_to_dict(setup)), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch setup: {str(e)}"}), 500

@app.route('/api/v1/setups', methods=['POST'])
def api_create_setup():
    """Create a new setup"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.json
        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        data['status'] = data.get('status', 'active')
        
        new_setup = Setup(**data)
        db.session.add(new_setup)
        db.session.commit()
        
        return jsonify(model_to_dict(new_setup)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create setup: {str(e)}"}), 500

@app.route('/api/v1/setups/<int:setup_id>', methods=['PUT'])
def api_update_setup(setup_id):
    """Update a setup"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        setup = db.session.get(Setup, setup_id)
        if not setup:
            return jsonify({"error": "Setup not found"}), 404
        
        data = request.json
        for key, value in data.items():
            if hasattr(setup, key):
                setattr(setup, key, value)
        
        db.session.commit()
        return jsonify(model_to_dict(setup)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update setup: {str(e)}"}), 500

@app.route('/api/v1/setups/<int:setup_id>', methods=['DELETE'])
def api_delete_setup(setup_id):
    """Delete a setup"""
    try:
        setup = db.session.get(Setup, setup_id)
        if not setup:
            return jsonify({"error": "Setup not found"}), 404
        
        db.session.delete(setup)
        db.session.commit()
        return jsonify({"message": "Setup deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete setup: {str(e)}"}), 500

# COMMANDS API
@app.route('/api/v1/commands', methods=['GET'])
def api_get_commands():
    """Get all commands"""
    try:
        commands = db.session.execute(db.select(Command).order_by(Command.id)).scalars().all()
        return jsonify([model_to_dict(command) for command in commands]), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch commands: {str(e)}"}), 500

@app.route('/api/v1/commands/<int:command_id>', methods=['GET'])
def api_get_command(command_id):
    """Get a specific command by ID"""
    try:
        command = db.session.get(Command, command_id)
        if not command:
            return jsonify({"error": "Command not found"}), 404
        return jsonify(model_to_dict(command)), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch command: {str(e)}"}), 500

@app.route('/api/v1/commands', methods=['POST'])
def api_create_command():
    """Create a new command"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.json
        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        data['status'] = data.get('status', 'pending')
        
        new_command = Command(**data)
        db.session.add(new_command)
        db.session.commit()
        
        return jsonify(model_to_dict(new_command)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create command: {str(e)}"}), 500

@app.route('/api/v1/commands/<int:command_id>', methods=['PUT'])
def api_update_command(command_id):
    """Update a command"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        command = db.session.get(Command, command_id)
        if not command:
            return jsonify({"error": "Command not found"}), 404
        
        data = request.json
        for key, value in data.items():
            if hasattr(command, key):
                setattr(command, key, value)
        
        db.session.commit()
        return jsonify(model_to_dict(command)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update command: {str(e)}"}), 500

@app.route('/api/v1/commands/<int:command_id>', methods=['DELETE'])
def api_delete_command(command_id):
    """Delete a command"""
    try:
        command = db.session.get(Command, command_id)
        if not command:
            return jsonify({"error": "Command not found"}), 404
        
        db.session.delete(command)
        db.session.commit()
        return jsonify({"message": "Command deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete command: {str(e)}"}), 500

# DEVICE COMMANDS API (for machine control)
@app.route('/api/v1/device/commands', methods=['POST'])
def api_device_command():
    """Execute device commands (e.g., start recipe)"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.json
        command_type = data.get("command")
        parameters = data.get("parameters", {})
        
        if command_type == "start_recipe":
            recipe_id = parameters.get("recipe_id")
            if recipe_id is None:
                return jsonify({"error": "Missing 'recipe_id' in parameters"}), 400
            
            # Find recipe
            recipe = db.session.get(Recipe, recipe_id)
            if not recipe:
                return jsonify({"error": f"Recipe id {recipe_id} not found"}), 404
            
            # Create command record
            command_entry = Command(
                name="start_recipe",
                description=f"Start recipe {recipe_id}: {recipe.description}",
                status="executing"
            )
            db.session.add(command_entry)
            db.session.commit()
            
            return jsonify({
                "status": "ok",
                "executed_command": model_to_dict(command_entry),
                "recipe_detail": recipe_to_dict(recipe)
            }), 201
        
        elif command_type == "reset":
            command_entry = Command(
                name="reset",
                description="Reset machine",
                status="executing"
            )
            db.session.add(command_entry)
            db.session.commit()
            
            return jsonify({
                "status": "ok",
                "executed_command": model_to_dict(command_entry)
            }), 201
        
        else:
            return jsonify({"error": "Unsupported command"}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to execute command: {str(e)}"}), 500

# API Documentation endpoint
@app.route('/api/v1/docs', methods=['GET'])
def api_docs():
    """API Documentation"""
    docs = {
        "api_version": "v1",
        "base_url": "/api/v1",
        "endpoints": {
            "contacts": {
                "GET /api/v1/contacts": "Get all contacts",
                "GET /api/v1/contacts/{id}": "Get contact by ID",
                "POST /api/v1/contacts": "Create new contact",
                "PUT /api/v1/contacts/{id}": "Update contact",
                "DELETE /api/v1/contacts/{id}": "Delete contact"
            },
            "wires": {
                "GET /api/v1/wires": "Get all wires",
                "GET /api/v1/wires/{id}": "Get wire by ID",
                "POST /api/v1/wires": "Create new wire",
                "PUT /api/v1/wires/{id}": "Update wire",
                "DELETE /api/v1/wires/{id}": "Delete wire"
            },
            "processes": {
                "GET /api/v1/processes": "Get all processes",
                "GET /api/v1/processes/{id}": "Get process by ID",
                "POST /api/v1/processes": "Create new process",
                "PUT /api/v1/processes/{id}": "Update process",
                "DELETE /api/v1/processes/{id}": "Delete process"
            },
            "recipes": {
                "GET /api/v1/recipes": "Get all recipes with full details",
                "GET /api/v1/recipes/{id}": "Get recipe by ID with full details",
                "POST /api/v1/recipes": "Create new recipe",
                "PUT /api/v1/recipes/{id}": "Update recipe",
                "DELETE /api/v1/recipes/{id}": "Delete recipe"
            },
            "jobs": {
                "GET /api/v1/jobs": "Get all jobs",
                "GET /api/v1/jobs/{id}": "Get job by ID",
                "POST /api/v1/jobs": "Create new job",
                "PUT /api/v1/jobs/{id}": "Update job",
                "DELETE /api/v1/jobs/{id}": "Delete job"
            },
            "setups": {
                "GET /api/v1/setups": "Get all setups",
                "GET /api/v1/setups/{id}": "Get setup by ID",
                "POST /api/v1/setups": "Create new setup",
                "PUT /api/v1/setups/{id}": "Update setup",
                "DELETE /api/v1/setups/{id}": "Delete setup"
            },
            "commands": {
                "GET /api/v1/commands": "Get all commands",
                "GET /api/v1/commands/{id}": "Get command by ID",
                "POST /api/v1/commands": "Create new command",
                "PUT /api/v1/commands/{id}": "Update command",
                "DELETE /api/v1/commands/{id}": "Delete command"
            },
            "device": {
                "POST /api/v1/device/commands": "Execute device commands (start_recipe, reset)"
            }
        },
        "data_format": "JSON",
        "authentication": "None (for demonstration)",
        "cors": "Enabled for all origins"
    }
    return jsonify(docs), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
