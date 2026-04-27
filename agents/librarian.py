from crewai import Agent
from tools.search_tools import internet_search

def get_librarian(llm="ollama/deepseek-v4-pro:cloud"):
    return Agent(
        role="Lead Technical Librarian & Standards Expert",
        goal="Synthesize a master document from 10+ sources, falling back to internal expertise for standards.",
        backstory="""You are an elite technical librarian. You MUST NOT ever state that
        standard protocols (SAML, OAuth, OIDC, SCIM, IPsec) are unresearchable.
        If your search tool returns no results, you are REQUIRED to use your extensive
        internal training data to provide expert-level technical details.
        Your synthesis must include protocol handshakes, trust establishment,
        and security hardening for every subpoint.""",
        llm=llm,
        tools=[internet_search],
        verbose=True
    )
