import streamlit as st
from market_research_system import MarketResearchSystem

def validate_api_keys(openai_key: str, tavily_key: str) -> bool:
    if not openai_key.startswith('sk-'):
        st.error("Invalid OpenAI API key")
        return False
    if not tavily_key.startswith('tvly-'):
        st.error("Invalid Tavily API key")
        return False
    return True

def main():
    st.set_page_config(
        page_title="AI Implementation Analysis",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("AI Implementation Analysis")
    st.write("Generate comprehensive AI implementation analysis with use cases, resources, and datasets")

    with st.form("analysis_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company = st.text_input(
                "Company Name",
                help="Enter the name of the company to analyze"
            )
            industry = st.text_input(
                "Industry",
                help="Enter the company's primary industry"
            )
            
        with col2:
            openai_api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                help="Enter your OpenAI API key (starts with 'sk-')"
            )
            tavily_api_key = st.text_input(
                "Tavily API Key",
                type="password",
                help="Enter your Tavily API key (starts with 'tvly-')"
            )
            
        with st.expander("Analysis Overview"):
            st.info("""
            This analysis will generate:
            - Practical AI Use Cases
            - Implementation Resources
            - Relevant Datasets
            - Code Repositories
            """)
            
        submitted = st.form_submit_button(
            "Generate Analysis",
            help="Click to start the analysis"
        )

    if submitted:
        if not all([company, industry, openai_api_key, tavily_api_key]):
            st.error("Please fill all required fields")
            return

        if not validate_api_keys(openai_api_key, tavily_api_key):
            return

        try:
            with st.spinner("Analyzing... This may take a few minutes..."):
                progress_text = st.empty()
                progress_text.text("Analysis in progress...")
                
                system = MarketResearchSystem(
                    company=company,
                    industry=industry,
                    openai_api_key=openai_api_key,
                    tavily_api_key=tavily_api_key
                )
                
                report, md_file, html_file = system.run()
                
                if report and md_file and html_file:
                    st.success("✅ Analysis completed!")
                    
                    tab1, tab2, tab3 = st.tabs([
                        "📊 Report",
                        "⬇️ Downloads",
                        "ℹ️ About"
                    ])
                    
                    with tab1:
                        st.markdown(report)
                    
                    with tab2:
                        st.write("### Download Options")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            with open(md_file, 'rb') as f:
                                st.download_button(
                                    "📄 Download Markdown",
                                    data=f,
                                    file_name=f"{company.lower()}_analysis.md",
                                    mime="text/markdown"
                                )
                        
                        with col2:
                            with open(html_file, 'rb') as f:
                                st.download_button(
                                    "🌐 Download HTML",
                                    data=f,
                                    file_name=f"{company.lower()}_analysis.html",
                                    mime="text/html"
                                )
                    
                    with tab3:
                        st.write("""
                        ### About This Analysis
                        
                        This analysis provides:
                        - Practical AI use cases
                        - Implementation resources
                        - Relevant datasets
                        - Code repositories
                        
                        Each use case includes:
                        - Detailed description
                        - Implementation guides
                        - Datasets and code
                        """)
                else:
                    st.error("Analysis generation failed")

        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
            st.warning("Please try again or contact support if the error persists.")

if __name__ == "__main__":
    main()