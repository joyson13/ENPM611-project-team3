# Import modules
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from model import Issue
from typing import List
from datetime import datetime, timezone
from data_loader import DataLoader

class SeverityAndImpactAnalysis:
    
    def __init__(self):
        """
        Constructor
        """
        self.issues: List[Issue] = DataLoader().get_issues()
        self.df = pd.DataFrame.from_records([issue.__dict__ for issue in self.issues])
        self.label_severity_mapping = {'Bug': 5, 'Needs Triage': 3, 'Feature': 1}
        self.state_severity_mapping = {'open': 2, 'closed': 0}
    
    def calculate_severity(self, issue):
        # Assign severity based on labels and state
        label_severity = sum(self.label_severity_mapping.get(label, 0) for label in issue['labels'])
        state_severity = self.state_severity_mapping.get(issue['state'], 0)
        
        # Duration factor based on issue age
        created_date = issue['created_date']
        now = datetime.now(timezone.utc)
        age_factor = (now - created_date).days if issue['state'] == 'open' else 0
        
        
        return label_severity + state_severity + (0.01 * age_factor)

    def calculate_impact(self, issue):
        # Calculate impact based on critical labels and events
        critical_labels = ['Bug', 'CI Failure']
        label_impact = sum(1 for label in issue['labels'] if label in critical_labels)
        event_impact = len(issue['events'])
        keyword_count = sum(issue['title'].count(keyword) + issue['text'].count(keyword) for keyword in critical_labels)
        
        return label_impact + event_impact + keyword_count

    def apply_analysis(self):
        # Apply severity and impact calculations to each issue
        self.df['severity_score'] = self.df.apply(self.calculate_severity, axis=1)
        self.df['impact_score'] = self.df.apply(self.calculate_impact, axis=1)
    
    def plot_severity_distribution(self):
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df['severity_score'], kde=True, color='skyblue')
        plt.title('Severity Score Distribution')
        plt.xlabel('Severity Score')
        plt.ylabel('Frequency')
        plt.show()

    def plot_impact_distribution(self):
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df['impact_score'], kde=True, color='coral')
        plt.title('Impact Score Distribution')
        plt.xlabel('Impact Score')
        plt.ylabel('Frequency')
        plt.show()

    def plot_severity_vs_impact(self):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='severity_score', y='impact_score', data=self.df, hue='state', palette="coolwarm")
        plt.title('Severity vs Impact of Issues')
        plt.xlabel('Severity Score')
        plt.ylabel('Impact Score')
        plt.show()

    def plot_keyword_heatmap(self, keyword):
        keyword_df = self.df[self.df['text'].str.contains(keyword, case=False) | self.df['title'].str.contains(keyword, case=False)]
        plt.figure(figsize=(8, 6))
        sns.heatmap(keyword_df.pivot_table(index='state', columns='severity_score', values='impact_score', aggfunc='count'), annot=True, cmap="YlGnBu")
        plt.title(f'Keyword Heatmap for "{keyword}"')
        plt.xlabel('Severity Score')
        plt.ylabel('State')
        plt.show()

    def run(self):
        """
        Entry point for severity and impact analysis
        """
        self.apply_analysis()
        
        # Basic statistics output
        print(f"Found {len(self.issues)} issues.")
        
        # Plotting visualizations
        self.plot_severity_distribution()
        self.plot_impact_distribution()
        self.plot_severity_vs_impact()
        
        # Example keyword for heatmap
        self.plot_keyword_heatmap(keyword="Bug")

if __name__ == '__main__':
    analysis = SeverityAndImpactAnalysis()
    analysis.run()
