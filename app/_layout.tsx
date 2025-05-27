// app/_layout.tsx
import { Slot, useRouter } from 'expo-router';
import { useState } from 'react';

export default function RootLayout() {
    // In a real app, use context or Redux for auth state
    // For demo, we'll use a simple state
    // We'll pass this state down via context or props
    // Here, just render the Slot (the router will handle grouping)
    return <Slot />;
}
