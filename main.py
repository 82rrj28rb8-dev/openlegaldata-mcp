import requests
from fastmcp import FastMCP

mcp = FastMCP("OpenLegalData Server")
BASE_URL = "https://de.openlegaldata.io/api/v1/cases/"

@mcp.tool()
def search_cases(query: str, limit: int = 3) -> str:
    """
    Sucht nach Gerichtsentscheidungen und Urteilen auf OpenLegalData.

    Args:
        query: Suchbegriff, Aktenzeichen oder Rechtsthema
        limit: Anzahl der Ergebnisse
    """
    try:
        response = requests.get(
            BASE_URL,
            params={"q": query, "page_size": limit},
            headers={"Accept": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        if not results:
            return f"Keine Urteile für die Anfrage '{query}' gefunden."

        formatted_output = f"### Suchergebnisse auf OpenLegalData für: '{query}'\n\n"

        for case in results:
            title = case.get("title") or "Ohne Titel"
            file_number = case.get("file_number") or "Unbekanntes Aktenzeichen"
            date = case.get("date") or "Unbekanntes Datum"
            court = case.get("court", {}).get("name") if isinstance(case.get("court"), dict) else "Unbekanntes Gericht"
            text_preview = case.get("content", "")[:500]

            formatted_output += f"**{title}**\n"
            formatted_output += f"- **Gericht:** {court}\n"
            formatted_output += f"- **Aktenzeichen:** {file_number}\n"
            formatted_output += f"- **Datum:** {date}\n"
            formatted_output += f"- **Auszug:** {text_preview}...\n\n---\n"

        return formatted_output

    except Exception as e:
        return f"Fehler bei der Abfrage von OpenLegalData: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
