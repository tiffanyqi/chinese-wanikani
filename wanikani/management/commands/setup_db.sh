echo "populating characters in database"
python3 manage.py populate_characters_in_db

echo "updating levels for populated characters"
python3 manage.py update_levels
