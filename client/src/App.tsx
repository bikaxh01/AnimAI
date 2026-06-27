import { useState, useEffect } from 'react';
import { Button } from './components/ui/button';
import { ProjectCard } from './components/ProjectCard';
import { api, type Project } from './services/api';

function App() {
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoadingProjects, setIsLoadingProjects] = useState(true);

  const fetchProjects = async () => {
    try {
      setIsLoadingProjects(true);
      const data = await api.listProjects();
      setProjects(data);
    } catch (error) {
      console.error('Failed to load projects:', error);
    } finally {
      setIsLoadingProjects(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      return;
    }

    try {
      setIsGenerating(true);
      const newProject = await api.createProject({ prompt });
      console.log('Project created:', newProject);
      setPrompt('');
      // Refresh the projects list to include the new one
      fetchProjects();
    } catch (error) {
      console.error('Failed to create project:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col items-center py-16 px-4 font-sans selection:bg-primary/30">
      
      <div className="w-full max-w-2xl mb-12">
        <h1 className="text-4xl font-bold text-center mb-10 text-primary">
          AnimAI Studio
        </h1>
        
        <div className="relative border border-border bg-card rounded-2xl focus-within:border-primary focus-within:ring-1 focus-within:ring-primary transition-all shadow-xl">
          <textarea 
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe the animation you want to generate..."
            className="w-full h-36 bg-transparent p-5 outline-none resize-none text-card-foreground placeholder:text-muted-foreground text-lg"
          />
          <div className="absolute bottom-4 right-4">
            <Button 
              onClick={handleGenerate} 
              disabled={isGenerating || !prompt.trim()}
              className="bg-primary hover:bg-primary/90 text-primary-foreground font-medium rounded-xl px-6 transition-all shadow-md disabled:opacity-50"
            >
              {isGenerating ? 'Generating...' : 'Generate'}
            </Button>
          </div>
        </div>
      </div>

      <div className="w-full max-w-2xl flex flex-col gap-6">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-xl font-semibold text-foreground">Recent Projects</h2>
        </div>
        
        {isLoadingProjects ? (
          <div className="text-muted-foreground text-center py-8">Loading projects...</div>
        ) : projects.length === 0 ? (
          <div className="text-muted-foreground text-center py-8 bg-card border border-border rounded-xl">
            No projects yet. Generate one above!
          </div>
        ) : (
          projects.map((project) => (
            <ProjectCard 
              key={project.id} 
              project={project}
            />
          ))
        )}
      </div>

    </div>
  )
}

export default App;
