'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import type { Todo, UpdateTodoRequest, ErrorResponse } from '@/types';


interface EditTodoPageState {
  todo: Todo | null;
  title: string;
  description: string;
  loading: boolean;
  error: string;
  saving: boolean;
}


export default function EditTodoPage() {
  const router = useRouter();
  const params = useParams();
  const todoId = params.id as string;

  const [state, setState] = useState<EditTodoPageState>({
    todo: null,
    title: '',
    description: '',
    loading: true,
    error: '',
    saving: false,
  });

  useEffect(() => {
    fetchTodo();
  }, [todoId]);

  const fetchTodo = async () => {
    setState(prev => ({ ...prev, loading: true, error: '' }));

    const response = await api.get<Todo>(`/todos/${todoId}`);

    if (response.error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: response.error || 'Failed to load todo',
      }));
      return;
    }

    if (response.data) {
      const todoData = response.data;
      setState(prev => ({
        ...prev,
        todo: todoData,
        title: todoData.title,
        description: todoData.description || '',
        loading: false,
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setState(prev => ({ ...prev, error: '', saving: true }));

    if (!state.title.trim()) {
      setState(prev => ({ ...prev, error: 'Title is required', saving: false }));
      return;
    }

    if (state.title.length > 200) {
      setState(prev => ({ ...prev, error: 'Title must be 200 characters or less', saving: false }));
      return;
    }

    const request: UpdateTodoRequest = {
      title: state.title.trim(),
      description: state.description.trim() || undefined,
    };

    const response = await api.put<Todo>(`/todos/${todoId}`, request);

    if (response.error) {
      setState(prev => ({ ...prev, error: response.error || 'Failed to update todo', saving: false }));
      return;
    }

    // Success - redirect to todos page
    router.push('/todos');
  };

  if (state.loading) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">Loading...</p>
      </div>
    );
  }

  if (state.error && !state.todo) {
    return (
      <div className="text-center py-8">
        <p className="text-red-600 mb-4">{state.error}</p>
        <Link href="/todos" className="text-blue-600 hover:underline">
          Back to Todos
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="flex items-center gap-4 mb-6">
        <Link href="/todos" className="text-gray-600 hover:text-gray-900">
          &larr; Back to Todos
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold mb-6">Edit Todo</h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          {state.error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {state.error}
            </div>
          )}

          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
              Title <span className="text-red-500">*</span>
            </label>
            <input
              id="title"
              type="text"
              value={state.title}
              onChange={(e) => setState(prev => ({ ...prev, title: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="What needs to be done?"
              maxLength={200}
              disabled={state.saving}
            />
            <p className="text-xs text-gray-500 mt-1">
              {state.title.length}/200 characters
            </p>
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
              Description (optional)
            </label>
            <textarea
              id="description"
              value={state.description}
              onChange={(e) => setState(prev => ({ ...prev, description: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 h-32"
              placeholder="Add more details..."
              maxLength={2000}
              disabled={state.saving}
            />
            <p className="text-xs text-gray-500 mt-1">
              {state.description.length}/2000 characters
            </p>
          </div>

          <div className="flex gap-4">
            <button
              type="submit"
              disabled={state.saving}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-blue-400 transition"
            >
              {state.saving ? 'Saving...' : 'Save Changes'}
            </button>
            <Link
              href="/todos"
              className="px-6 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition"
            >
              Cancel
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
