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
        tag = coil_details[1]  # Use coil_details[1] to get the coil tag
        
        # Check if the tag already exists in the database
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM coil WHERE tag = %s", (tag,))
        existing_coil = cursor.fetchone()
        
        if existing_coil: 
            return f"Coil Tag {tag} already exists"
        
        coil_details += ('New',) 
        query = """
        INSERT INTO coil (tag, supplier, color, gauge, weight, location, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, coil_details)
        db.commit()
        cursor.close()
        db.close()

    except mysql.connector.Error as err:
        return f"An error occurred while inserting the coil data: {err}"


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