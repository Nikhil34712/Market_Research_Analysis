# Streamlit UI implementation for Market Research System
import streamlit as st
from market_research_system import MarketResearchSystem

# Validate API key formats
def validate_api_keys(openai_key: str, tavily_key: str) -> bool:
    # Check OpenAI API key format
    if not openai_key.startswith('sk-'):
        st.error("Invalid OpenAI API key")
        return False
    # Check Tavily API key format    
    if not tavily_key.startswith('tvly-'):
        st.error("Invalid Tavily API key")
        return False
    return True

def main():
    # Configure Streamlit page settings
    st.set_page_config(
        page_title="AI Implementation Analysis",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Main title and description
    st.title("AI Implementation Analysis")
    st.write("Generate comprehensive AI implementation analysis with use cases, resources, and datasets")

    # Create input form
    with st.form("analysis_form"):
        # Split form into two columns
        col1, col2 = st.columns(2)
        
        # Column 1: Company and Industry inputs
        with col1:
            company = st.text_input(
                "Company Name",
                help="Enter the name of the company to analyze"
            )
            industry = st.text_input(
                "Industry",
                help="Enter the company's primary industry"
            )
        
        # Column 2: API key inputs    
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
        
        # Expandable section explaining the analysis process    
        with st.expander("Analysis Process"):
            st.info("""
            This analysis generates:
            
            1. Use Cases Analysis
            • 4 High-Impact AI Use Cases
            • Clear Problem Statements
            • Business Benefits
            • Implementation Complexity
            
            2. Implementation Resources
            • Official Company Documentation
            • Product Guides & Tools
            • Technical Frameworks
            
            3. Datasets & Code
            • Real, Accessible Datasets
            • Implementation Code
            • Training Materials
            
            4. Comprehensive Guide
            • Detailed Implementation Steps
            • Resource Integration
            • Best Practices
            """)
            
        # Submit button    
        submitted = st.form_submit_button(
            "Generate Analysis",
            help="Click to start the analysis"
        )

    # Handle form submission
    if submitted:
        # Validate all required fields
        if not all([company, industry, openai_api_key, tavily_api_key]):
            st.error("Please fill all required fields")
            return

        # Validate API key formats
        if not validate_api_keys(openai_api_key, tavily_api_key):
            return

        try:
            # Show analysis progress
            with st.spinner("Generating comprehensive analysis..."):
                progress_container = st.empty()
                
                def update_progress(stage):
                    progress_container.info(f"Current Stage: {stage}")
                
                update_progress("Identifying optimal use cases...")
                
                # Initialize and run market research system
                system = MarketResearchSystem(
                    company=company,
                    industry=industry,
                    openai_api_key=openai_api_key,
                    tavily_api_key=tavily_api_key
                )
                
                # Generate reports
                report, md_file, html_file = system.run()
                
                # Display results if generation successful
                if report and md_file and html_file:
                    st.success("✅ Analysis completed successfully!")
                    
                    # Create three tabs for different views
                    tab1, tab2, tab3 = st.tabs([
                        "📊 Analysis Report",
                        "⬇️ Download Options",
                        "ℹ️ Implementation Guide"
                    ])
                    
                    # Tab 1: Display analysis report
                    with tab1:
                        st.markdown(report)
                    
                    # Tab 2: Download options
                    with tab2:
                        st.write("### Download Analysis Report")
                        col1, col2 = st.columns(2)
                        
                        # Markdown download button
                        with col1:
                            with open(md_file, 'rb') as f:
                                st.download_button(
                                    "📄 Download Markdown Report",
                                    data=f,
                                    file_name=f"{company.lower()}_analysis.md",
                                    mime="text/markdown",
                                    help="Download the report in Markdown format for easy editing"
                                )
                        
                        # HTML download button
                        with col2:
                            with open(html_file, 'rb') as f:
                                st.download_button(
                                    "🌐 Download HTML Report",
                                    data=f,
                                    file_name=f"{company.lower()}_analysis.html",
                                    mime="text/html",
                                    help="Download the report in HTML format for web viewing"
                                )
                    
                    # Tab 3: Implementation guide
                    with tab3:
                        st.write("""
                        ### Implementation Guide
                        
                        This analysis provides:
                        
                        #### Use Cases
                        • Detailed problem statements
                        • Clear business benefits
                        • Implementation complexity assessment
                        
                        #### Resources
                        • Official company documentation
                        • Implementation guides
                        • Technical frameworks
                        
                        #### Datasets & Code
                        • Real, accessible datasets
                        • Implementation code
                        • Training materials
                        
                        All resources have been verified to ensure they are:
                        • Currently accessible
                        • Relevant to use cases
                        • From reliable sources
                        """)
                else:
                    st.error("Analysis generation failed")
                    st.warning("Please check your inputs and try again")

        # Handle errors
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
            st.warning("""
            If you encounter this error:
            1. Verify your API keys
            2. Check your internet connection
            3. Try again in a few moments
            """)

# Run the Streamlit app
if __name__ == "__main__":
    main()