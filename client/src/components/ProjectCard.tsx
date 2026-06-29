import React, { useState, useEffect } from 'react';
import { api, type Project } from '../services/api';
import { Button } from './ui/button';

export type ProjectStatus =
  | 'pending'
  | 'planning'
  | 'writing_script'
  | 'storyboarding'
  | 'generating_code'
  | 'analyzing_code'
  | 'debugging'
  | 'compiling'
  | 'completed'
  | 'failed';

export interface ProjectCardProps {
  project: Project;
}

const getStatusConfig = (status: string) => {
  switch (status) {
    case 'completed':
      return { label: 'Completed', styles: 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20' };
    case 'failed':
      return { label: 'Failed', styles: 'bg-destructive/10 text-destructive border-destructive/20' };
    case 'pending':
      return { label: 'Pending', styles: 'bg-neutral-500/10 text-neutral-400 border-neutral-500/20' };
    case 'planning':
      return { label: 'Planning', styles: 'bg-blue-500/10 text-blue-500 border-blue-500/20' };
    case 'writing_script':
      return { label: 'Writing Script', styles: 'bg-indigo-500/10 text-indigo-500 border-indigo-500/20' };
    case 'storyboarding':
      return { label: 'Storyboarding', styles: 'bg-purple-500/10 text-purple-500 border-purple-500/20' };
    case 'generating_code':
      return { label: 'Generating Code', styles: 'bg-pink-500/10 text-pink-500 border-pink-500/20' };
    case 'analyzing_code':
      return { label: 'Analyzing Code', styles: 'bg-cyan-500/10 text-cyan-500 border-cyan-500/20' };
    case 'debugging':
      return { label: 'Debugging', styles: 'bg-orange-500/10 text-orange-500 border-orange-500/20' };
    case 'compiling':
      return { label: 'Compiling', styles: 'bg-amber-500/10 text-amber-500 border-amber-500/20' };
    default:
      return { label: status, styles: 'bg-neutral-500/10 text-neutral-400 border-neutral-500/20' };
  }
};

export const ProjectCard: React.FC<ProjectCardProps> = ({ project: initialProject }) => {
  const [project, setProject] = useState<Project>(initialProject);

  useEffect(() => {
    let intervalId: ReturnType<typeof setInterval>;

    const pollProject = async () => {
      try {
        const updatedProject = await api.getProject(project.id);
        setProject(updatedProject);
      } catch (error) {
        console.error('Failed to poll project status:', error);
      }
    };

    if (project.status !== 'completed' && project.status !== 'failed') {
      intervalId = setInterval(pollProject, 3000); // Poll every 3 seconds
    }

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [project.id, project.status]);

  const { label, styles } = getStatusConfig(project.status);

  const title = project.title || "Untitled Project";
  const description = project.description || project.prompt;

  return (
    <div className="border border-border rounded-xl p-5 bg-card w-full hover:border-primary/50 transition-colors shadow-sm">
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-lg font-semibold text-card-foreground">{title}</h3>
        <span className={`px-2.5 py-1 text-xs font-medium rounded-full border ${styles}`}>
          {label}
        </span>
      </div>
      <p className="text-muted-foreground text-sm mb-4 leading-relaxed line-clamp-2" title={description}>{description}</p>

      {project.code_file && (
        <div className="mb-4 flex">
          <Button variant="outline" size="sm" className="ml-auto" onClick={() => window.open(project.code_file!, '_blank')}>
            View Code
          </Button>
        </div>
      )}

      {project.video_url ? (
        <div className="mt-4 rounded-lg overflow-hidden bg-black aspect-video flex items-center justify-center border border-border">
          <video src={project.video_url} controls className="w-full h-full object-cover" />
        </div>
      ) : (
        <div className="mt-4 rounded-lg overflow-hidden bg-muted/20 aspect-video flex items-center justify-center border border-border/50">
          <span className="text-muted-foreground text-sm">
            {project.status === 'failed' ? 'Generation failed' : 'No video available'}
          </span>
        </div>
      )}
    </div>
  );
};
