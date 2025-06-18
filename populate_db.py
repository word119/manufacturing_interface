from main import app, db, Contact, Wire, Process, Recipe, Job, Setup, Command
from datetime import datetime

def populate_database():
    with app.app_context():
        # Clear existing data
        db.session.query(Recipe).delete()
        db.session.query(Contact).delete()
        db.session.query(Wire).delete()
        db.session.query(Process).delete()
        db.session.query(Job).delete()
        db.session.query(Setup).delete()
        db.session.query(Command).delete()
        
        # Add Contacts
        contacts_data = [
            {
                "Description": "Alpha",
                "Diameter": "12.34",
                "Insertdepth": "22.10",
                "Name": "ZF001",
                "ZF_ContNumb": "5.789"
            },
            {
                "Description": "Beta",
                "Diameter": "14.78",
                "Insertdepth": "24.50",
                "Name": "ZF002",
                "ZF_ContNumb": "6.123"
            },
            {
                "Description": "Gamma",
                "Diameter": "16.90",
                "Insertdepth": "26.78",
                "Name": "ZF003",
                "ZF_ContNumb": "7.456"
            },
            {
                "Description": "Delta",
                "Diameter": "18.25",
                "Insertdepth": "28.90",
                "Name": "ZF004",
                "ZF_ContNumb": "8.234"
            },
            {
                "Description": "Epsilon",
                "Diameter": "20.10",
                "Insertdepth": "30.12",
                "Name": "ZF005",
                "ZF_ContNumb": "9.876"
            }
        ]
        
        for contact_data in contacts_data:
            contact = Contact(**contact_data)
            db.session.add(contact)
        
        # Add Wires
        wires_data = [
            {
                "name": "W001",
                "description": "Standard copper wire",
                "cross_section": "0.5 mm²",
                "isolation_diameter": "1.2 mm",
                "wire_diameter": "0.8 mm",
                "color": "red"
            },
            {
                "name": "W002",
                "description": "Shielded wire",
                "cross_section": "0.75 mm²",
                "isolation_diameter": "1.5 mm",
                "wire_diameter": "1.0 mm",
                "color": "blue"
            },
            {
                "name": "W003",
                "description": "Flexible wire",
                "cross_section": "1.0 mm²",
                "isolation_diameter": "1.6 mm",
                "wire_diameter": "1.1 mm",
                "color": "green"
            },
            {
                "name": "W004",
                "description": "High voltage wire",
                "cross_section": "1.5 mm²",
                "isolation_diameter": "2.0 mm",
                "wire_diameter": "1.3 mm",
                "color": "black"
            },
            {
                "name": "W005",
                "description": "Tinned wire",
                "cross_section": "2.0 mm²",
                "isolation_diameter": "2.4 mm",
                "wire_diameter": "1.6 mm",
                "color": "white"
            }
        ]
        
        for wire_data in wires_data:
            wire = Wire(**wire_data)
            db.session.add(wire)
        
        # Add Processes
        processes_data = [
            {
                "name": "P001",
                "crimping_depth_d": "1.0",
                "crimping_depth_offset_d": "0.2",
                "holding_value_delta_d": "0.05",
                "insertion_depth_delta_d": "0.1",
                "sf_performance_d": "95",
                "sf_frequence_d": "60Hz",
                "extendable_feeder_tuble_s": "yes",
                "loading_holding_jaws_s": "standard",
                "catact_monitoring_s": "enabled",
                "wayback_d": "3.5",
                "stripping_position": "front",
                "stripping_function": "auto",
                "crimping_position_monitoring": "enabled"
            },
            {
                "name": "P002",
                "crimping_depth_d": "1.1",
                "crimping_depth_offset_d": "0.15",
                "holding_value_delta_d": "0.06",
                "insertion_depth_delta_d": "0.09",
                "sf_performance_d": "93",
                "sf_frequence_d": "50Hz",
                "extendable_feeder_tuble_s": "no",
                "loading_holding_jaws_s": "heavy",
                "catact_monitoring_s": "disabled",
                "wayback_d": "4.0",
                "stripping_position": "rear",
                "stripping_function": "manual",
                "crimping_position_monitoring": "disabled"
            },
            {
                "name": "P003",
                "crimping_depth_d": "1.2",
                "crimping_depth_offset_d": "0.25",
                "holding_value_delta_d": "0.07",
                "insertion_depth_delta_d": "0.11",
                "sf_performance_d": "90",
                "sf_frequence_d": "45Hz",
                "extendable_feeder_tuble_s": "yes",
                "loading_holding_jaws_s": "medium",
                "catact_monitoring_s": "enabled",
                "wayback_d": "3.2",
                "stripping_position": "front",
                "stripping_function": "auto",
                "crimping_position_monitoring": "enabled"
            },
            {
                "name": "P004",
                "crimping_depth_d": "1.3",
                "crimping_depth_offset_d": "0.3",
                "holding_value_delta_d": "0.08",
                "insertion_depth_delta_d": "0.12",
                "sf_performance_d": "92",
                "sf_frequence_d": "55Hz",
                "extendable_feeder_tuble_s": "no",
                "loading_holding_jaws_s": "light",
                "catact_monitoring_s": "disabled",
                "wayback_d": "4.1",
                "stripping_position": "rear",
                "stripping_function": "manual",
                "crimping_position_monitoring": "enabled"
            },
            {
                "name": "P005",
                "crimping_depth_d": "1.4",
                "crimping_depth_offset_d": "0.35",
                "holding_value_delta_d": "0.09",
                "insertion_depth_delta_d": "0.13",
                "sf_performance_d": "94",
                "sf_frequence_d": "65Hz",
                "extendable_feeder_tuble_s": "yes",
                "loading_holding_jaws_s": "standard",
                "catact_monitoring_s": "enabled",
                "wayback_d": "3.8",
                "stripping_position": "front",
                "stripping_function": "auto",
                "crimping_position_monitoring": "enabled"
            }
        ]
        
        for process_data in processes_data:
            process = Process(**process_data)
            db.session.add(process)
        
        # Commit to get IDs
        db.session.commit()
        
        # Add Recipes
        recipes_data = [
            {
                "description": "First assembly",
                "contact_id": 1,
                "wire_id": 1,
                "process_id": 1
            },
            {
                "description": "Second assembly",
                "contact_id": 2,
                "wire_id": 2,
                "process_id": 2
            },
            {
                "description": "Third assembly",
                "contact_id": 3,
                "wire_id": 3,
                "process_id": 3
            },
            {
                "description": "Fourth assembly",
                "contact_id": 4,
                "wire_id": 4,
                "process_id": 4
            },
            {
                "description": "Fifth assembly",
                "contact_id": 5,
                "wire_id": 5,
                "process_id": 5
            }
        ]
        
        for recipe_data in recipes_data:
            recipe = Recipe(**recipe_data)
            db.session.add(recipe)
        
        # Add some sample Jobs, Setups, and Commands
        job_data = {
            "name": "Sample Job 1", 
            "status": "pending", 
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        job = Job(**job_data)
        db.session.add(job)
        
        setup_data = {
            "name": "Default Setup", 
            "description": "Standard manufacturing setup", 
            "status": "active"
        }
        setup = Setup(**setup_data)
        db.session.add(setup)
        
        command_data = {
            "name": "Start Process", 
            "description": "Initialize manufacturing process", 
            "status": "pending"
        }
        command = Command(**command_data)
        db.session.add(command)
        
        # Final commit
        db.session.commit()
        
        print("Database populated successfully!")

if __name__ == "__main__":
    populate_database() 