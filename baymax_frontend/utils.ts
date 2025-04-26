import Constants from 'expo-constants';

export const BASE_API_URL = process.env.NODE_ENV === 'development' 
  ? 'http://localhost:8000' 
  : process.env.EXPO_PUBLIC_API_BASE_URL || '';

export const generateAPIUrl = (relativePath: string) => {
  const path = relativePath.startsWith('/') ? relativePath : `/${relativePath}`;
  return `${BASE_API_URL}${path}`;
}; 