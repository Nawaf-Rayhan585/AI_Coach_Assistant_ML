import json
import numpy as np
from sklearn.neighbors import NearestNeighbors
import subprocess

# Use Ollama locally to get embeddings
def get_embedding(text: str):
    """
    Get embedding vector from Ollama for a given text.
    Raises RuntimeError if Ollama fails or returns invalid output.
    """
    try:
        result = subprocess.run(
            ["ollama", "embeddings", "--model", "llama3.2:1b", text],
            capture_output=True,
            text=True,   # get stdout as string
            check=True   # raises CalledProcessError if CLI fails
        )

        if not result.stdout.strip():
            raise RuntimeError("Ollama returned empty output. Check if the model is installed and CLI works.")

        data = json.loads(result.stdout)
        if "embedding" not in data:
            raise RuntimeError(f"No 'embedding' key in Ollama response: {data}")

        return np.array(data["embedding"], dtype=np.float32)

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Ollama CLI error: {e}\nOutput: {e.output}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse Ollama output as JSON: {e}\nOutput: {result.stdout}")

class CareerAgent:
    def __init__(self, jobs_path="data/jobs.json"):
        with open(jobs_path, "r", encoding="utf-8") as f:
            self.jobs = json.load(f)
        self._build_index()

    def _build_index(self):
        texts = [j["title"] + " -- " + j["description"] for j in self.jobs]
        embeddings_list = []

        for i, t in enumerate(texts):
            try:
                emb = get_embedding(t)
                embeddings_list.append(emb)
            except Exception as e:
                print(f"[Warning] Failed to get embedding for job {i}: {e}")
                embeddings_list.append(np.zeros(1536, dtype=np.float32))  # fallback embedding size (adjust to your model)

        self.embeddings = np.vstack(embeddings_list)
        norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True) + 1e-10
        self.normalized = self.embeddings / norms
        self.nn = NearestNeighbors(n_neighbors=5, metric="euclidean")
        self.nn.fit(self.normalized)

    def recommend_roles(self, user_text, k=3):
        try:
            emb = get_embedding(user_text)
            emb_norm = emb / (np.linalg.norm(emb) + 1e-10)
        except Exception as e:
            print(f"[Warning] Failed to get embedding for user text: {e}")
            emb_norm = np.zeros(self.embeddings.shape[1], dtype=np.float32)

        distances, idxs = self.nn.kneighbors([emb_norm], n_neighbors=k)
        results = []
        for dist, i in zip(distances[0], idxs[0]):
            job = self.jobs[i]
            sim = 1 - dist
            results.append({"job": job, "score": float(sim)})
        return results

    def summary_for_prompt(self, top_roles):
        blocks = []
        for r in top_roles:
            job = r["job"]
            blocks.append(f"- {job['title']}: {job['description']} (tags: {', '.join(job['tags'])})")
        return "\n".join(blocks)

    def generate_plan(self, background, top_roles):
        summary = self.summary_for_prompt(top_roles)
        system_prompt = (
            "You are an expert AI career coach. Given a user's background and possible job roles, "
            "produce:\n1. Best matched role and reason.\n2. Key skills to learn.\n"
            "3. 3/6/12-month learning roadmap with milestones.\n4. Example projects to build.\n"
            "Be practical and concise."
        )

        prompt = f"User background:\n{background}\n\nTop roles:\n{summary}\n\nNow create the plan."

        try:
            result = subprocess.run(
                ["ollama", "run", "llama3.2:3b"],
                input=(system_prompt + "\n" + prompt).encode("utf-8"),
                capture_output=True,
                check=True
            )
            return result.stdout.decode("utf-8")
        except subprocess.CalledProcessError as e:
            print(f"[Error] Ollama run failed: {e}")
            return "Failed to generate plan. Please check Ollama setup."
