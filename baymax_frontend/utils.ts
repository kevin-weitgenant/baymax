import Constants from 'expo-constants';
import { Platform } from 'react-native';

// Use your computer's local IP address instead of localhost
const LOCAL_IP = '192.168.0.103'; 

export const BASE_API_URL = process.env.NODE_ENV === 'development' 
  ? Platform.OS === 'web' 
    ? 'http://localhost:8000'
    : `http://${LOCAL_IP}:8000`
  : process.env.EXPO_PUBLIC_API_BASE_URL || '';

export const generateAPIUrl = (relativePath: string) => {
  const path = relativePath.startsWith('/') ? relativePath : `/${relativePath}`;
  return `${BASE_API_URL}${path}`;
}; 