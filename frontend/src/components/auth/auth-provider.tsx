'use client';

import { createContext, useContext, useState, ReactNode } from 'react';
import { initAuthState, saveAuthState, clearAuthState, type AuthState, type User, type Session } from '@/lib/auth-client';


interface AuthContextType extends AuthState {
  signin: (user: User, session: Session) => void;
  signout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);


export function AuthProvider({ children }: { children: ReactNode }) {
  // Initialize auth state synchronously from localStorage to prevent flickering
  const initialState = initAuthState();
  const [authState, setReactAuthState] = useState<AuthState>(initialState);

  const signin = (user: User, session: Session) => {
    // Store in localStorage and update React state
    saveAuthState(user, session);
    setReactAuthState({
      user,
      session,
      isLoading: false,
      isAuthenticated: true,
    });
  };

  const signout = () => {
    // Clear localStorage and update React state
    clearAuthState();
    setReactAuthState({
      user: null,
      session: null,
      isLoading: false,
      isAuthenticated: false,
    });
  };

  return (
    <AuthContext.Provider value={{ ...authState, signin, signout }}>
      {children}
    </AuthContext.Provider>
  );
}


export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
