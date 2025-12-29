'use client';

import { useState } from 'react';
import { Button } from '../ui/button';


interface DeleteConfirmProps {
  todoId: string;
  todoTitle: string;
  onDelete: (todoId: string) => Promise<void>;
  onCancel: () => void;
}


export function DeleteConfirm({ todoId, todoTitle, onDelete, onCancel }: DeleteConfirmProps) {
  const [loading, setLoading] = useState(false);

  const handleDelete = async () => {
    setLoading(true);
    await onDelete(todoId);
    setLoading(false);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-sm mx-4">
        <h3 className="text-lg font-semibold mb-2">Delete Todo</h3>
        <p className="text-gray-600 mb-4">
          Are you sure you want to delete &quot;{todoTitle}&quot;? This action cannot be undone.
        </p>
        <div className="flex justify-end gap-3">
          <Button
            variant="secondary"
            onClick={onCancel}
            disabled={loading}
          >
            Cancel
          </Button>
          <Button
            variant="danger"
            onClick={handleDelete}
            loading={loading}
          >
            Delete
          </Button>
        </div>
      </div>
    </div>
  );
}
