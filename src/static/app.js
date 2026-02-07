document.addEventListener("DOMContentLoaded", () => {
  const activitiesContainer = document.getElementById("activities-container");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesContainer.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([activityName, activityData]) => {
        const participantsList = activityData.participants
          .map((p) => `<li>${p}</li>`)
          .join("");

        const participantsHTML =
          activityData.participants.length > 0
            ? participantsList
            : '<li class="no-participants">No participants yet</li>';

        const card = document.createElement("div");
        card.className = "activity-card";
        card.innerHTML = `
                <h3>${activityName}</h3>
                <p class="description">${activityData.description}</p>
                <p class="schedule"><strong>Schedule:</strong> ${activityData.schedule}</p>
                <p class="capacity"><strong>Capacity:</strong> ${activityData.participants.length}/${activityData.max_participants}</p>
                
                <div class="participants-section">
                    <h4>Participants (${activityData.participants.length})</h4>
                    <ul class="participants-list">
                        ${participantsHTML}
                    </ul>
                </div>
                
                <button class="signup-btn" onclick="signupForActivity('${activityName}')">Sign Up</button>
            `;

        activitiesContainer.appendChild(card);
      });
    } catch (error) {
      activitiesContainer.innerHTML =
        "<p class='error'>Failed to load activities</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Sign up for an activity
  window.signupForActivity = async (activityName) => {
    const email = prompt("Enter your email:");
    if (!email) return;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activityName)}/signup?email=${encodeURIComponent(
          email
        )}`,
        {
          method: "POST",
        }
      );

      if (response.ok) {
        alert("Successfully signed up!");
        fetchActivities();
      } else {
        const error = await response.json();
        alert(`Error: ${error.detail}`);
      }
    } catch (error) {
      console.error("Error signing up:", error);
      alert("Failed to sign up. Please try again.");
    }
  };

  // Initialize app
  fetchActivities();
});
