import pandas as pd

from connect import connect


def read_data(filename: str):
    """
    Get data from database.

    :param filename: Name of the file to be read.
    """
    data = pd.read_excel(filename)

    data.rename(columns={'active_energy': 'value'}, inplace=True)
    data['meter_date'] = data['meter_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    data.drop(columns=['meter_id'], inplace=True)

    return data


# Connect with Firebase:
def save_data(data: pd.DataFrame):
    """
    Save data to database.

    :param data: Data to be saved.
    """
    collection = connect()

    documents = data.to_dict('records')

    collection.insert_many(documents)


def main():
    """
    Main function.
    """
    filename = 'data.xlsx'
    data = read_data(filename)
    save_data(data)


if __name__ == '__main__':
    main()
