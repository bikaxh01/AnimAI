const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export interface CreateProjectPayload {
  prompt: string;
}

export interface Project {
  id: string;
  title: string | null;
  description: string | null;
  code_file: string | null;
  video_url: string | null;
  prompt: string;
  status: 'pending' | 'planning' | 'writing_script' | 'storyboarding' | 'generating_code' | 'analyzing_code' | 'debugging' | 'compiling' | 'completed' | 'failed';
  created_at: string;
  updated_at: string;
}

export const api = {
  createProject: async (data: CreateProjectPayload): Promise<Project> => {
    const response = await fetch(`${API_BASE_URL}/projects/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      throw new Error(`Failed to create project: ${response.statusText}`);
    }
    
    return response.json();
  },

  listProjects: async (): Promise<Project[]> => {
    const response = await fetch(`${API_BASE_URL}/projects/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (!response.ok) {
      throw new Error(`Failed to list projects: ${response.statusText}`);
    }

    return response.json();
  },

  getProject: async (pid: string): Promise<Project> => {
    const response = await fetch(`${API_BASE_URL}/projects/${pid}/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (!response.ok) {
      throw new Error(`Failed to get project: ${response.statusText}`);
    }

    return response.json();
  }
};
