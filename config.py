import mysql.connector
import logging

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ekanban"
    )

def insert_new_coil_to_db(coil_details):
    try:
        tag = coil_details[1]
        
        db = connect_db()
        cursor = db.cursor()
        
        cursor.execute("SELECT * FROM coil WHERE tag = %s", (tag,))
        existing_coil = cursor.fetchone()
        
        if existing_coil:
            cursor.close()
            db.close()
            return f"Coil Tag {tag} already exists. No new entry added."

        coil_details += ('New',)
        
        query = """
        INSERT INTO coil (tag, supplier, color, gauge, weight, location, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, coil_details)
            db.commit()
            return f"Coil Tag {tag} added successfully."
        except mysql.connector.IntegrityError as err:
            if err.errno == 1062:
                return f"Duplicate entry for Coil Tag {tag}"
            else:
                return f"An error occurred during insertion: {err}"
        
        cursor.close()
        db.close()

    except mysql.connector.Error as err:
        return f"Database error: {err}"


def get_coil_tag_from_db():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM coil;")
    tags = cursor.fetchall()

    cursor.close()
    db.close()

    return tags

def search_coil_tag_job_order(search_term):
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT * FROM coil WHERE tag LIKE %s"
    cursor.execute(query, (f"%{search_term}%",))
    results = cursor.fetchall()
    cursor.close()
    db.close()

    return results

def get_coil_detail_per_tag(coil_tag):
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT * FROM coil WHERE tag = %s;"
    cursor.execute(query, (coil_tag,))
    coil_details = cursor.fetchone()
    cursor.close()
    db.close()

    return coil_details

def get_coil_detail_per_tag_operator(coil_tag):
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT * FROM coil WHERE tag = %s;"
    cursor.execute(query, (coil_tag,))
    coil_details = cursor.fetchone()
    cursor.close()
    db.close()

    return coil_details

def delete(coil_tag):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM coil WHERE tag = %s", (coil_tag,))
        db.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False

    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")
        db.rollback()
        return False
        
    finally:
        cursor.close()
        db.close()

def issue(coil_tag):
    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("UPDATE coil SET status = 'To do' WHERE tag = %s", (coil_tag,))
        
        db.commit()
        cursor.close()
        db.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
        cursor.close()
        db.close()
        return f"An error occurred while updating the coil status: {err}"

    return "success"

def operator_todo_coil_tags():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM coil WHERE status= 'To do'")
    tags = cursor.fetchall()
    cursor.close()
    db.close()

    return tags

def operator_inprog_coil_tags():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM coil WHERE status= 'In progress'")
    tags = cursor.fetchall()
    cursor.close()
    db.close()

    return tags

def operator_done_coil_tags():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM coil WHERE status= 'Done'")
    tags = cursor.fetchall()
    cursor.close()
    db.close()

    return tags

def done(coil_tag, weight):

    try:
        db = connect_db()
        cursor = db.cursor()
        status = "Used"  # Default status
        
        if weight  == 0:
            status = "EOC"
        
        # Update the coil's status in the database
        cursor.execute("UPDATE coil SET status = %s WHERE tag = %s", (status, coil_tag))
        db.commit()
        cursor.close()
        db.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
        cursor.close()
        db.close()
        return f"An error occurred while updating the coil status: {err}"

    return "success"

def cancel_inprog(coil_tag):
    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("UPDATE coil SET status = 'To do' WHERE tag = %s", (coil_tag,))
        
        db.commit()
        cursor.close()
        db.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
        cursor.close()
        db.close()
        return f"An error occurred while updating the coil status: {err}"

    return "success"

def cancel(coil_tag):
    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("UPDATE coil SET status = 'In progress' WHERE tag = %s", (coil_tag,))
        
        db.commit()
        cursor.close()
        db.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
        cursor.close()
        db.close()
        return f"An error occurred while updating the coil status: {err}"

    return "success"

def start(coil_tag):
    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("UPDATE coil SET status = 'In progress' WHERE tag = %s", (coil_tag,))
        
        db.commit()
        cursor.close()
        db.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
        cursor.close()
        db.close()
        return f"An error occurred while updating the coil status: {err}"

    return "success"

def edit(to_edit, coil_tag):
    try:
        db = connect_db()
        cursor = db.cursor()
        query = """
            UPDATE coil 
            SET location = %s, weight = %s, status = 'Done' 
            WHERE tag = %s
        """
        cursor.execute(query, (*to_edit, coil_tag)) 
        db.commit()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
        return f"An error occurred while updating the coil status: {err}"
    
    finally:
        cursor.close()
        db.close()

    return "success"