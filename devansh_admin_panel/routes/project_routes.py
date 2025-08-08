

from flask import Blueprint, request, jsonify
from flask_login import login_required
from db.connection import mysql
import json

project_bp = Blueprint('project_bp', __name__)

# Get all projects
@project_bp.route('/', methods=['GET'])
@login_required
def get_projects():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    cursor.close()

    result = []
    for project in projects:
        result.append({
            'id': project[0],
            'title': project[1],
            'description': project[2],
            'category': project[3],
            'image_urls': project[4].split(',') if project[4] else [],
            'created_at': project[5].strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(result)

# Add a new project
@project_bp.route('/', methods=['POST'])
@login_required
def add_project():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    category = data.get('category')
    image_urls = ','.join(data.get('image_urls', []))

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO projects (title, description, category, image_urls) VALUES (%s, %s, %s, %s)",
                   (title, description, category, image_urls))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Project added successfully'}), 201

# Delete a project
@project_bp.route('/<int:project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM projects WHERE id = %s", (project_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Project deleted successfully'}), 200