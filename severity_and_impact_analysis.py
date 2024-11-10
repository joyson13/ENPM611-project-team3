# Import modules
import re
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
        
        total_severity_score = label_severity + state_severity + (0.01 * age_factor)
        return total_severity_score

    def calculate_impact(self, issue):
        # Calculate impact based on critical labels and events
        critical_labels = ['Bug', 'CI Failure']
        label_impact = sum(1 for label in issue['labels'] if label in critical_labels)
        event_impact = len(issue['events'])
        
        for keyword in critical_labels:
            count_in_title = 0 if issue['title'] is None else len(re.findall(keyword, issue["title"], re.IGNORECASE))
            count_in_text = 0 if issue['text'] is None else len(re.findall(keyword, issue["text"], re.IGNORECASE))

        keyword_count = count_in_title + count_in_text
        
        return label_impact + event_impact + keyword_count

    def apply_analysis(self):
        # Apply severity and impact calculations to each issue
        self.df['severity_score'] = self.df.apply(self.calculate_severity, axis=1)
        self.df['impact_score'] = self.df.apply(self.calculate_impact, axis=1)
    
    # Plot of impact distribution
    def plot_severity_distribution(self):
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df['severity_score'], kde=True, color='skyblue')
        plt.title('Severity Score Distribution')
        plt.xlabel('Severity Score')
        plt.ylabel('Frequency')
        plt.show()

    # Plot of impact distribution
    def plot_impact_distribution(self):
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df['impact_score'], kde=True, color='coral')
        plt.title('Impact Score Distribution')
        plt.xlabel('Impact Score')
        plt.ylabel('Frequency')
        plt.show()

    # Plot of severity vs impact
    def plot_severity_vs_impact(self):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='severity_score', y='impact_score', data=self.df, hue='state', palette="coolwarm")
        plt.title('Severity vs Impact of Issues')
        plt.xlabel('Severity Score')
        plt.ylabel('Impact Score')
        plt.show()

    def fetch_and_plot(self):
                
        # Basic statistics output
        print(f"Found {len(self.issues)} issues.")
        
        # Generate features
        self.apply_analysis()
        
        # Plotting visualizations
        self.plot_severity_distribution()
        self.plot_impact_distribution()
        self.plot_severity_vs_impact()


if __name__ == '__main__':
    # fetch and plot method when running this module directly
    SeverityAndImpactAnalysis().fetch_and_plot()