import pandas as pd
import matplotlib.pyplot as plt
from data_loader import DataLoader

class ContributorAndAssigneeAnalysis:
    """
    Analyzes contributors and assignees from GitHub issues and visualizes the results.
    """

    def __init__(self):
        """
        Constructor
        """
        self.issues = DataLoader().get_issues()  # Load issues using DataLoader

    def fetch_and_plot(self):
        # Ask user for the number of contributors and assignees to display
        top_contributors_count = int(input("Enter the number of contributors to display: "))
        top_assignees_count = int(input("Enter the number of assignees to display: "))

        contributor_counts = {}
        assignee_counts = {}

        for issue in self.issues:
            # Count contributors
            contributor = issue.creator
            contributor_counts[contributor] = contributor_counts.get(contributor, 0) + 1

            # Count assignees
            for assignee in issue.assignees:
                assignee_username = assignee['login']  # Ensure to extract correctly
                assignee_counts[assignee_username] = assignee_counts.get(assignee_username, 0) + 1

        # Create DataFrames from counts
        contributor_df = pd.DataFrame(list(contributor_counts.items()), columns=['Contributor', 'Issue Count'])
        assignee_df = pd.DataFrame(list(assignee_counts.items()), columns=['Assignee', 'Issue Count'])

        # Plot both contributors and assignees on the same page
        self.plot_analysis(contributor_df, assignee_df, top_contributors_count, top_assignees_count)

    def plot_analysis(self, contributor_df: pd.DataFrame, assignee_df: pd.DataFrame, top_contributors_count: int, top_assignees_count: int):
        # Create subplots with 1 row and 2 columns
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

        # Plot contributors
        contributor_df = contributor_df.nlargest(top_contributors_count, 'Issue Count')
        axes[0].barh(contributor_df['Contributor'], contributor_df['Issue Count'], color='skyblue')
        axes[0].set_title('Top Contributors')
        axes[0].set_xlabel('Number of Issues')
        axes[0].set_ylabel('Contributors')

        # Add count labels on the bars
        for index, value in enumerate(contributor_df['Issue Count']):
            axes[0].text(value, index, int(value), va='center')  # va: vertical alignment

        # Plot assignees
        assignee_df = assignee_df.nlargest(top_assignees_count, 'Issue Count')
        axes[1].barh(assignee_df['Assignee'], assignee_df['Issue Count'], color='salmon')
        axes[1].set_title('Top Assignees')
        axes[1].set_xlabel('Number of Issues')
        axes[1].set_ylabel('Assignees')

        # Add count labels on the bars
        for index, value in enumerate(assignee_df['Issue Count']):
            axes[1].text(value, index, int(value), va='center')  # va: vertical alignment

        # Adjust layout
        plt.tight_layout()
        plt.show()
