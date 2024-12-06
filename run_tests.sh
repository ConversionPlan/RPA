DIRECTORY="Track_RPA/tests"

for file in $DIRECTORY/*; do
  if [[ -f "$file" ]]; then
    python "$file"
  fi
done