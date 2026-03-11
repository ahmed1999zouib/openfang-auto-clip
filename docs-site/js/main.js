const revealObserver = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("is-visible");
            }
        });
    },
    {
        threshold: 0.12,
    }
);

document.querySelectorAll(".reveal").forEach((element) => {
    revealObserver.observe(element);
});

document.querySelectorAll("[data-copy-target]").forEach((button) => {
    button.addEventListener("click", async () => {
        const target = document.getElementById(button.dataset.copyTarget);
        if (!target) {
            return;
        }

        try {
            await navigator.clipboard.writeText(target.textContent);
            const originalText = button.textContent;
            button.textContent = "Copied";
            setTimeout(() => {
                button.textContent = originalText;
            }, 1400);
        } catch (error) {
            console.error("Failed to copy command", error);
        }
    });
});

async function updateRepositorySignal() {
    try {
        const response = await fetch("https://api.github.com/repos/outhsics/openfang-auto-clip");
        if (!response.ok) {
            throw new Error(`GitHub API responded with ${response.status}`);
        }

        const data = await response.json();
        document.getElementById("starCount").textContent = data.stargazers_count;
        document.getElementById("forkCount").textContent = data.forks_count;
        document.getElementById("updatedAt").textContent = new Date(data.updated_at).toLocaleDateString("en-CA");
    } catch (error) {
        console.error("Failed to load repository signal", error);
        document.getElementById("starCount").textContent = "GitHub";
        document.getElementById("forkCount").textContent = "signal";
        document.getElementById("updatedAt").textContent = "live";
    }
}

updateRepositorySignal();
