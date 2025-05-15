import camelot

tables = camelot.read_pdf(
    "/home/mswed/Documents/coding/springboard/capstone2/backend/grumpytracker/cameras/ALEXA 35 _ formats.pdf"
)

df = tables[0].df
print(df)

# Export to CSV for inspection
tables[0].to_csv("alexa_formats.csv")
