def load_queries(file_path):
    import csv

    queries = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            queries.append(row['Search Query'])
    return queries