import pandas as pd

class ChunkIterator:
    def __init__(self, file_path, chunk_size=100):
        """
        Initialize the ChunkIterator.
        :param file_path: Path to the dataset CSV file.
        :param chunk_size: Number of rows to process in each chunk.
        """
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.iterator = pd.read_csv(self.file_path, chunksize=self.chunk_size)

    def __iter__(self):
        """
        Make the ChunkIterator class iterable.
        """
        return self

    def __next__(self):
        """
        Return the next chunk of data.
        """
        try:
            chunk = next(self.iterator)
        except StopIteration:
            # Raise StopIteration when there are no more chunks
            raise StopIteration
        return chunk

    def calculate_statistics(self, chunk):
        """
        Calculate basic statistics (mean, median) for numerical columns in the chunk.
        :param chunk: A chunk of the dataset.
        :return: A dictionary containing statistics.
        """
        stats = {}
        for column in chunk.select_dtypes(include=['float64', 'int64']):
            stats[column] = {
                'mean': chunk[column].mean(),
                'median': chunk[column].median(),
                'min': chunk[column].min(),
                'max': chunk[column].max(),
            }
        return stats
def process_dataset(file_path, chunk_size):
    # Initialize the ChunkIterator with the dataset path and chunk size
    chunk_iterator = ChunkIterator(file_path, chunk_size)
    
    for chunk in chunk_iterator:
        print("Processing a new chunk...")
        
        # Calculate statistics for the current chunk
        stats = chunk_iterator.calculate_statistics(chunk)
        
        # Print the statistics for each chunk
        for column, column_stats in stats.items():
            print(f"Statistics for column: {column}")
            for stat, value in column_stats.items():
                print(f"{stat.capitalize()}: {value}")
            print("-" * 40)

if __name__ == "__main__":
    # Path to the dataset
    file_path = "Mall_Customers.csv"
    
    # Set the chunk size (number of rows to process at a time)
    chunk_size = 50
    
    # Process the dataset in chunks and print statistics for each chunk
    process_dataset(file_path, chunk_size)