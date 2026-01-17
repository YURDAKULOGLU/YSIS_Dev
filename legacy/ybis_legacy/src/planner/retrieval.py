from src.memory.structure import retrieveMemory

def get_relevant_info(query: str) -> str:
    """
    Retrieve relevant information from memory based on the query.

    Args:
        query (str): The query to search for in memory.

    Returns:
        str: Relevant information retrieved from memory.
    """
    return retrieveMemory(query)
