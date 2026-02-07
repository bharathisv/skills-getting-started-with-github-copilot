document.addEventListener("DOMContentLoaded", () => {
  const activitiesContainer = document.getElementById("activities-container");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities", { cache: "no-store" });
      const activities = await response.json();

      // Clear loading message
      activitiesContainer.innerHTML = "";

      // reset activity select so options don't accumulate
      if (activitySelect) {
        activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';
      }

      // Populate activities list
      Object.entries(activities).forEach(([activityName, activityData]) => {
        const card = document.createElement("div");
        card.className = "activity-card";
        card.innerHTML = `
            <h3>${activityName}</h3>
            <p class="description">${activityData.description}</p>
            <p class="schedule"><strong>Schedule:</strong> ${activityData.schedule}</p>
            <p class="capacity"><strong>Capacity:</strong> ${activityData.participants.length}/${activityData.max_participants}</p>
                
            <div class="participants-section">
              <h4>Participants (${activityData.participants.length})</h4>
              <ul class="participants-list"></ul>
            </div>
          `;

        // add signup button and wire up listener
        const btn = document.createElement("button");
        btn.className = "signup-btn";
        btn.type = "button";
        btn.textContent = "Sign Up";
        btn.addEventListener("click", () => signupForActivity(activityName));
        card.appendChild(btn);

        // populate participants list with delete buttons
        const ul = card.querySelector('.participants-list');
        if (Array.isArray(activityData.participants) && activityData.participants.length > 0) {
          activityData.participants.forEach((p) => {
            const li = document.createElement('li');

            const span = document.createElement('span');
            span.className = 'participant-email';
            span.textContent = p;
            li.appendChild(span);

            const del = document.createElement('button');
            del.className = 'delete-participant';
            del.type = 'button';
            del.title = 'Unregister participant';
            del.innerHTML = '✖';
            del.addEventListener('click', (e) => {
              e.stopPropagation();
              if (confirm(`Unregister ${p} from ${activityName}?`)) {
                unregisterParticipant(activityName, p);
              }
            });

            li.appendChild(del);
            ul.appendChild(li);
          });
        } else {
          const li = document.createElement('li');
          li.className = 'no-participants';
          li.textContent = 'No participants yet';
          ul.appendChild(li);
        }

        activitiesContainer.appendChild(card);
        // populate select option
        if (activitySelect) {
          const opt = document.createElement("option");
          opt.value = activityName;
          opt.textContent = activityName;
          activitySelect.appendChild(opt);
        }
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
        await fetchActivities();
      } else {
        const error = await response.json();
        alert(`Error: ${error.detail}`);
      }
    } catch (error) {
      console.error("Error signing up:", error);
      alert("Failed to sign up. Please try again.");
    }
  };

  // Unregister a participant
  window.unregisterParticipant = async (activityName, email) => {
    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activityName)}/participants?email=${encodeURIComponent(email)}`,
        { method: 'DELETE' }
      );

      const result = await response.json();
      if (response.ok) {
        alert(result.message || 'Participant unregistered');
        await fetchActivities();
      } else {
        alert(result.detail || 'Failed to unregister participant');
      }
    } catch (err) {
      console.error('Error unregistering participant:', err);
      alert('Failed to unregister. Please try again.');
    }
  };


  // handle signup form submission (if present)
  if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("email").value;
      const activity = document.getElementById("activity").value;
      if (!activity || !email) return;

      try {
        const response = await fetch(
          `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
          { method: "POST" }
        );

        const result = await response.json();
        if (response.ok) {
          if (messageDiv) {
            messageDiv.textContent = result.message;
            messageDiv.className = "message success";
            messageDiv.classList.remove("hidden");
          }
          signupForm.reset();
          await fetchActivities();
        } else {
          if (messageDiv) {
            messageDiv.textContent = result.detail || "An error occurred";
            messageDiv.className = "message error";
            messageDiv.classList.remove("hidden");
          }
        }
        setTimeout(() => messageDiv && messageDiv.classList.add("hidden"), 4000);
      } catch (err) {
        console.error("Error signing up via form:", err);
        if (messageDiv) {
          messageDiv.textContent = "Failed to sign up. Please try again.";
          messageDiv.className = "message error";
          messageDiv.classList.remove("hidden");
        }
      }
    });
  }

  // Initialize app
  fetchActivities();
});
