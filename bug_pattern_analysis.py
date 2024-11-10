import config
import pandas as pd
import matplotlib.pyplot as plt
from typing import List
from data_loader import DataLoader
from model import Issue, Event

class BugPatternsAnalysis:
    """
    Analyzes bug patterns and frequency from GitHub issues, optionally by a specific creator.
    """

    def __init__(self):
        """Constructor"""
        self.bug_keywords = ['bug', 'error', 'fail', 'exception', 'crash', 'not working', 'unexpected']
        self.user = config.get_parameter('user')  # Get the optional user label

    def run(self):
        """Starting point for the bug pattern analysis."""
        issues: List[Issue] = DataLoader().get_issues()

        if self.user:
            # Analyze bug patterns for the specific creator if a user label is provided
            self.analyze_bug_patterns_for_creator(issues)
        else:
            # Otherwise, show the general bug patterns frequency
            self.analyze_general_bug_patterns(issues)

    def analyze_general_bug_patterns(self, issues: List[Issue]):
        """Analyzes and plots bug patterns frequency across all issues."""
        bug_patterns_count = {}

        # Loop through issues to detect keywords in titles or labels and count occurrences
        for issue in issues:
            issue_text = (issue.title + ' ' + ' '.join(issue.labels)).lower()
            for keyword in self.bug_keywords:
                if keyword in issue_text:
                    bug_patterns_count[keyword] = bug_patterns_count.get(keyword, 0) + 1

        # Sort and print the results
        bug_patterns_count = sorted(bug_patterns_count.items(), key=lambda x: x[1], reverse=True)
        print("\n\nGeneral Bug Patterns and Frequency Analysis:\n")
        for keyword, count in bug_patterns_count:
            print(f"{keyword.capitalize()}: {count} occurrences")

        # Plot the bar chart
        if bug_patterns_count:
            bug_patterns_df = pd.DataFrame(bug_patterns_count, columns=['Pattern', 'Frequency'])
            bug_patterns_chart = bug_patterns_df.set_index('Pattern').plot(
                kind='bar', 
                figsize=(12, 6), 
                title="Bug Patterns and Their Frequency"
            )
            plt.xlabel("Bug Patterns")
            plt.ylabel("Frequency")

            for bar in bug_patterns_chart.patches:
                bug_patterns_chart.annotate(
                    f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', 
                    va='bottom', 
                    fontsize=10, 
                    color='black'
                )
            plt.show()
        else:
            print("No bug patterns found.\n")

    def analyze_bug_patterns_for_creator(self, issues: List[Issue]):
        """Analyzes and plots bug patterns frequency for a specific creator."""
        creator_bug_patterns = {}

        # Filter issues for the specified creator and detect keywords in titles or labels
        for issue in issues:
            if issue.creator == self.user:
                issue_text = (issue.title + ' ' + ' '.join(issue.labels)).lower()
                for keyword in self.bug_keywords:
                    if keyword in issue_text:
                        creator_bug_patterns[keyword] = creator_bug_patterns.get(keyword, 0) + 1

        # Sort and print results for the specified creator
        creator_bug_patterns = sorted(creator_bug_patterns.items(), key=lambda x: x[1], reverse=True)
        print(f"\n\nBug Patterns and Frequency Analysis for Creator '{self.user}':\n")
        for keyword, count in creator_bug_patterns:
            print(f"{keyword.capitalize()}: {count} occurrences")

        # Plot the bar chart for the specified creator
        if creator_bug_patterns:
            creator_bug_patterns_df = pd.DataFrame(creator_bug_patterns, columns=['Pattern', 'Frequency'])
            creator_bug_patterns_chart = creator_bug_patterns_df.set_index('Pattern').plot(
                kind='bar', 
                figsize=(12, 6), 
                title=f"Bug Patterns for Creator '{self.user}'"
            )
            plt.xlabel("Bug Patterns")
            plt.ylabel("Frequency")

            for bar in creator_bug_patterns_chart.patches:
                creator_bug_patterns_chart.annotate(
                    f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', 
                    va='bottom', 
                    fontsize=10, 
                    color='black'
                )
            plt.show()
        else:
            print(f"No bug patterns found for creator '{self.user}'.\n")

if __name__ == "__main__":
    BugPatternsAnalysis().run()
