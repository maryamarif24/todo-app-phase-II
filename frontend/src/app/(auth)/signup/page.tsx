import { SignupForm } from '@/components/auth/signup-form';
import Link from 'next/link';

export default function SignupPage() {
  return (
    <div className="bg-white rounded-lg shadow-md p-8">
      <h1 className="text-2xl font-bold text-center mb-6" style={{ color: "#7F1734" }}>Create Account</h1>
      <SignupForm />
      <p className="mt-4 text-center text-sm" style={{ color: "#7F1734" }}>
        Already have an account?{' '}
        <Link href="/signin" className="text-blue-600 hover:underline">
          Sign in
        </Link>
      </p>
    </div>
  );
}
