import streamlit as st
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi
import hashlib
from bson import ObjectId

st.set_page_config(layout="wide", page_title="Price Data Project", page_icon="✌")

st.header('Database Management', divider='red')
st.subheader('')

# Database connection setup
uri1 = "mongodb+srv://btinsley:pricedataproject@cluster0.dch9w5y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
uri2 = "mongodb+srv://btinsley:pricedataproject@price-publications-1.kfhfx.mongodb.net/?retryWrites=true&w=majority&appName=price-publications-1"
client1 = MongoClient(uri1, server_api=ServerApi('1'))
client2 = MongoClient(uri2, server_api=ServerApi('1'))

def get_client_based_on_author(name):
    hash_object = hashlib.md5(name.encode())
    hash_number = int(hash_object.hexdigest(), 16)
    return client1 if hash_number % 2 == 0 else client2

all_fields = ['name', 'title', 'year', 'citation', "Authors", "Publication date", "Journal",
              "Volume", "Issue", "Pages", "Publisher", "Description", 'type']

if 'fields' not in st.session_state:
    st.session_state.fields = [['name', ''], ['title', ''], ['year', '']]

st.title("Add Publication")

# Add field functionality
def get_available_fields(selected_fields):
    return [field for field in all_fields if field not in selected_fields]

if st.button("Add Field"):
    used_fields = [field[0] for field in st.session_state.fields]
    available_fields = get_available_fields(used_fields)
    if available_fields:
        st.session_state.fields.append([available_fields[0], ''])

# Form to create a new publication
with st.form(key='create_publication_form'):
    used_fields = set()
    for i, field in enumerate(st.session_state.fields):
        col1, col2 = st.columns(2)
        with col1:
            current_field = field[0]
            available_options = get_available_fields([f[0] for f in st.session_state.fields if f[0] != current_field] + list(used_fields))
            if current_field not in available_options:
                available_options.append(current_field)
            available_options.sort(key=lambda x: all_fields.index(x))
            field[0] = st.selectbox("", available_options, index=available_options.index(current_field), key=f'field_{i}')
        with col2:
            field[1] = st.text_input("", value=field[1], key=f'value_{i}')
        used_fields.add(field[0])
    submitted = st.form_submit_button("Submit Publication")

if submitted:
    document = {field[0]: field[1] for field in st.session_state.fields if field[0] and field[1]}
    if document:
        client = get_client_based_on_author(document.get('name', ''))
        db = client['publications']
        collection = db['articles']
        try:
            collection.insert_one(document)
            st.success("Publication inserted successfully into the database!")
        except errors.DuplicateKeyError:
            st.error("A document with that name and title already exists.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please ensure all fields are filled correctly.")



st.title("Search Publications")
with st.form("search_form"):
    selected_field = st.selectbox("Select field to search by:", all_fields)
    query_value = st.text_input("Enter search value:")
    search_submitted = st.form_submit_button("Search")

if search_submitted and query_value:
    if selected_field == 'name':
        client = get_client_based_on_author(query_value)
        results = list(client['publications']['articles'].find({selected_field: {'$regex': query_value, '$options': 'i'}}))
    else:
        # If not searching by name, search both databases and merge the results
        results1 = list(client1['publications']['articles'].find({selected_field: {'$regex': query_value, '$options': 'i'}}))
        results2 = list(client2['publications']['articles'].find({selected_field: {'$regex': query_value, '$options': 'i'}}))
        results = results1 + results2
    if not results:
        st.write(f"No results found for {selected_field} \"{query_value}\".")
    else:
        for result in results:
            result_str = '\n'.join([f"{key}: {value}" for key, value in result.items()])
            st.text(result_str)




def get_document(doc_id):
    """ Retrieve a document from both databases. """
    for client in [client1, client2]:
        db = client['publications']
        collection = db['articles']
        document = collection.find_one({'_id': ObjectId(doc_id)})
        if document:
            return document, client
    return None, None

def delete_document(doc_id, client):
    """ Delete a document from a specified database. """
    collection = client['publications']['articles']
    result = collection.delete_one({'_id': ObjectId(doc_id)})
    if result.deleted_count > 0:
        return "Document deleted successfully."
    return "Failed to delete the document or document not found."

st.title("Delete Publication")
doc_id_to_delete = st.text_input("Enter the document ID to delete:")

if doc_id_to_delete:
    document, client_used = get_document(doc_id_to_delete)
    if document:
        st.write("Article Details:")
        for key, value in document.items():
            st.text(f"{key}: {value}")

        delete_confirmed = st.button("Delete Document")
        if delete_confirmed:
            try:
                ObjectId(doc_id_to_delete)  # Validates if the input is a valid ObjectId
                deletion_result = delete_document(doc_id_to_delete, client_used)
                st.success(deletion_result)
            except Exception as e:
                st.error("Failed to delete the document. Error: " + str(e))
    else:
        st.error("No document found with that ID.")
else:
    st.write("Please enter a document ID to proceed.")



def update_document(doc_id, updates, client):
    """ Update the document with new data in the specified client's database. """
    db = client['publications']
    collection = db['articles']
    try:
        result = collection.update_one({'_id': ObjectId(doc_id)}, {'$set': updates})
        return result.modified_count > 0
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    

st.title("Update Publication")
doc_id_input = st.text_input("Enter Document ID to Update:")

if doc_id_input:
    document, client_used = get_document(doc_id_input)
    if document:
        # Create session state for form data if necessary
        if 'form_data' not in st.session_state or st.session_state.get('update_clicked', False):
            st.session_state.form_data = {key: str(value) for key, value in document.items() if key != '_id'}
            st.session_state['update_clicked'] = False

        # Display editable text inputs for each document field
        updated_data = {}
        for key, value in st.session_state.form_data.items():
            updated_data[key] = st.text_input(key.capitalize(), value)

        if st.button("Update Document"):
            if update_document(doc_id_input, updated_data, client_used):
                st.success("Document updated successfully!")
                st.session_state['update_clicked'] = True
            else:
                st.error("Failed to update document.")
    else:
        st.error("No document found with that ID.")
else:
    st.write("Please enter a document ID.")