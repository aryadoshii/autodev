// src/components/PriorityList.jsx
import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { PriorityService } from '../services/PriorityService';

const PriorityList = () => {
  // State management
  const [priorities, setPriorities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  
  // Form states
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    color: '#3b82f6'
  });
  
  const [editingId, setEditingId] = useState(null);
  const [errors, setErrors] = useState({});

  // Context
  const { user } = useAuth();

  // Fetch priorities on component mount
  useEffect(() => {
    fetchPriorities();
  }, []);

  // Fetch all priorities
  const fetchPriorities = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await PriorityService.getAll();
      setPriorities(data);
    } catch (err) {
      setError('Failed to fetch priorities');
      console.error('Error fetching priorities:', err);
    } finally {
      setLoading(false);
    }
  };

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  // Validate form
  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }
    
    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      if (editingId) {
        // Update existing priority
        const updatedPriority = await PriorityService.update(editingId, formData);
        setPriorities(prev => 
          prev.map(p => p.id === editingId ? updatedPriority : p)
        );
        setSuccessMessage('Priority updated successfully');
      } else {
        // Create new priority
        const newPriority = await PriorityService.create(formData);
        setPriorities(prev => [...prev, newPriority]);
        setSuccessMessage('Priority created successfully');
      }
      
      // Reset form
      resetForm();
    } catch (err) {
      setError('Failed to save priority');
      console.error('Error saving priority:', err);
    } finally {
      setLoading(false);
    }
  };

  // Edit priority
  const handleEdit = (priority) => {
    setFormData({
      name: priority.name,
      description: priority.description,
      color: priority.color || '#3b82f6'
    });
    setEditingId(priority.id);
  };

  // Delete priority
  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this priority?')) {
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      await PriorityService.delete(id);
      setPriorities(prev => prev.filter(p => p.id !== id));
      setSuccessMessage('Priority deleted successfully');
    } catch (err) {
      setError('Failed to delete priority');
      console.error('Error deleting priority:', err);
    } finally {
      setLoading(false);
    }
  };

  // Reset form
  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      color: '#3b82f6'
    });
    setEditingId(null);
    setErrors({});
  };

  // Cancel edit
  const handleCancel = () => {
    resetForm();
  };

  // Render loading state
  if (loading && priorities.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Priority Management</h1>
        <p className="text-gray-600 mt-2">Manage your task priorities</p>
      </div>

      {/* Success Message */}
      {successMessage && (
        <div className="mb-6 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
          <span className="block sm:inline">{successMessage}</span>
          <button 
            onClick={() => setSuccessMessage(null)}
            className="absolute top-0 bottom-0 right-0 px-4 py-3"
          >
            <span className="text-green-500 hover:text-green-700">&times;</span>
          </button>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mb-6 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <span className="block sm:inline">{error}</span>
          <button 
            onClick={() => setError(null)}
            className="absolute top-0 bottom-0 right-0 px-4 py-3"
          >
            <span className="text-red-500 hover:text-red-700">&times;</span>
          </button>
        </div>
      )}

      {/* Form Section */}
      <div className="bg-white shadow-md rounded-lg p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">
          {editingId ? 'Edit Priority' : 'Add New Priority'}
        </h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                Name *
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 ${
                  errors.name ? 'border-red-500 focus:ring-red-200' : 'border-gray-300 focus:ring-blue-200'
                }`}
                placeholder="Enter priority name"
              />
              {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name}</p>}
            </div>
            
            <div>
              <label htmlFor="color" className="block text-sm font-medium text-gray-700 mb-1">
                Color
              </label>
              <div className="flex items-center space-x-2">
                <input
                  type="color"
                  id="color"
                  name="color"
                  value={formData.color}
                  onChange={handleInputChange}
                  className="w-10 h-10 border border-gray-300 rounded cursor-pointer"
                />
                <span className="text-sm text-gray-600">{formData.color}</span>
              </div>
            </div>
          </div>
          
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
              Description *
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows="3"
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 ${
                errors.description ? 'border-red-500 focus:ring-red-200' : 'border-gray-300 focus:ring-blue-200'
              }`}
              placeholder="Enter priority description"
            />
            {errors.description && <p className="mt-1 text-sm text-red-600">{errors.description}</p>}
          </div>
          
          <div className="flex space-x-3 pt-2">
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Saving...
                </span>
              ) : editingId ? 'Update Priority' : 'Add Priority'}
            </button>
            
            {editingId && (
              <button
                type="button"
                onClick={handleCancel}
                className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
              >
                Cancel
              </button>
            )}
          </div>
        </form>
      </div>

      {/* Priorities List */}
      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-800">Priority List</h2>
        </div>
        
        {loading && priorities.length > 0 ? (
          <div className="flex justify-center items-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : priorities.length === 0 ? (
          <div className="py-12 text-center">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">No priorities</h3>
            <p className="mt-1 text-sm text-gray-500">Get started by creating a new priority.</p>
          </div>
        ) : (
          <ul className="divide-y divide-gray-200">
            {priorities.map((priority) => (
              <li key={priority.id} className="px-6 py-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div 
                      className="w-4 h-4 rounded-full" 
                      style={{ backgroundColor: priority.color }}
                    ></div>
                    <div>
                      <h3 className="text-lg font-medium text-gray-900">{priority.name}</h3>
                      <p className="text-sm text-gray-500">{priority.description}</p>
                    </div>
                  </div>
                  
                  <div className="flex space-x-3">
                    <button
                      onClick={() => handleEdit(priority)}
                      className="text-blue-600 hover:text-blue-900 focus:outline-none"
                      title="Edit"
                    >
                      <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth