# Charles River Economics Labs @UChicago -- Fall 2023, Census Bureau
This is our GitHub repository for the Fall 2023 UChicago project. We are working with the US Census Bureau Associate Director of Economic Programs (ADEP) on this semester-long project.

Key Question: How does the legalization and growth of the cannabis industry at national and subnational levels affect economic indicators, business dynamics, and worker demographics? To this end, how can we generate a novel dataset to encompass the cannabis industry?

The cannabis industry has seen rapid growth in recent years, with an array of recreational and medicinal markets, varying state legalizations, and diverse business models emerging. While there exists significant public, administrative, and third-party data about businesses in this supply chain, a systematic and comprehensive approach to understanding the economic impact of the cannabis industry is lacking. This project aims to fill this gap in the data and enhance our understanding of industry business patterns using descriptive econometric analysis. Ultimately, we hope to reveal novel insights on how cannabis businesses influence the broader economic landscape, worker demographics, and business dynamics in regions where they operate.

Objectives
Establish a robust database of cannabis businesses by probabilistically linking available data sources.
Analyze the growth trajectory of cannabis businesses in different states, comparing early adopters of legalization to late ones.
Examine how the presence of cannabis businesses influences regional employment, revenue generation, and business dynamics.
Analyze the demography of the cannabis industry, focusing on business owners and employees.

Methodology: Data Construction, Linkage, Preliminary Analysis
Using tools and platforms recommended by the Census, we attempt to create a comprehensive dataset by linking administrative, public, and third-party data sources with internal business data. The Census will provide us with a probabilistic linkage procedure which primarily matches business names and addresses, which can be used as a starting point.

We conduct an additional analysis on business growth and the impact of legality.  To this end, we plan to use state licensure data to track the formation and dissolution of cannabis businesses over time. This allows us to analyze business growth in relation to legalization timelines, distinguishing between medicinal and recreational markets. Finally, we compare business trajectories across states, focusing on pioneers like California and Colorado which can identify cross-state influences.

Methodology: Economic Impact Analysis using PSM
Propensity Score Matching (PSM) is a causal inference method used for estimating treatment effects when treatment assignment is non-random, and selection bias may be present. We can apply this framework to estimate the effect of cannabis legalization on business growth. By matching states/counties that legalized cannabis to similar states/counties that did not (based on observable characteristics), we should be able to estimate a causal effect of legalization.

Using the novel data frame that we create, we follow a general process:
Economic Modeling/Intuition: Identify key trends and inconsistencies in the data across-states. For example, let’s say the data tells us that legal states exhibit greater business growth than states in which marijuana is illegal. In this case, do the states that fully legalize differ in observable characteristics like political inclination or economic growth trajectory, from states that do not legalize? Could the observed differences in growth be due to these inherent differences, rather than the legalization?
Econometric Modeling: Note that in the above scenario, we cannot observe what would have happened in a treated (legalized) state if it were never treated. PSM circumvents this problem by creating a counterfactual. We match each treated state with a non-treated state that has a similar propensity to legalize, based on observable characteristics. The potential outcomes framework comes in handy here. For each unit, we observe Yi(1) = outcome for unit i if treated OR Yi(0) = outcome for unit i if not treated, but not both. We seek to recover the Average Treatment Effect (ATE), which in this case ATE = E[Yi(1) - Yi(0)].

Forthcoming are the specific details for propensity score estimation, logistic regression, matching, covariate distribution comparison, and treatment effect estimation. This seems to be a useful approach given the (presumed) structure of our data and the objectives of this project, but is certainly subject to change.

Communication and Collaboration:
Maintain regular communication with the Census Bureau through weekly full-team meetings and ensure timely feedback integration.
Share findings via presentations and check-ins with key Census stakeholders, i.e. Katie and Rebecca.
Ensure that the project's findings and insights are presented in a manner consistent with the Census Bureau's expectations, starting with data creation and culminating in a rigorous statistical/econometric analysis.

Expected Outcomes
We aim to deliver a holistic understanding of the cannabis industry's economic impact in several dimensions.
We will produce valuable insights for policymakers, industry stakeholders, and other researchers. As with all of our work at EcLabs, the findings will inform public policies and strategic industry decisions.
