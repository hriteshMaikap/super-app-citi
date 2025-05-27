import { Tabs } from 'expo-router';
import { Ionicons, MaterialCommunityIcons, FontAwesome5, Feather } from '@expo/vector-icons';

export default function TabsLayout() {
    return (
        <Tabs>
            <Tabs.Screen
                name="home"
                options={{
                    title: 'HOME',
                    tabBarIcon: ({ focused, color, size }) => (
                        <Ionicons name="home" size={size ?? 24} color={focused ? "#007AFF" : "#888"} />
                    ),
                }}
            />
            <Tabs.Screen
                name="Chats"
                options={{
                    title: 'CHAT',
                    tabBarIcon: ({ focused, color, size }) => (
                        <Ionicons name="chatbubbles" size={size ?? 24} color={focused ? "#007AFF" : "#888"} />
                    ),
                }}
            />
            <Tabs.Screen
                name="payments"
                options={{
                    title: 'PAY',
                    tabBarIcon: ({ focused, color, size }) => (
                        <MaterialCommunityIcons name="credit-card-outline" size={size ?? 24} color={focused ? "#007AFF" : "#888"} />
                    ),
                }}
            />
            <Tabs.Screen
                name="shopping"
                options={{
                    title: 'SHOP',
                    tabBarIcon: ({ focused, color, size }) => (
                        <FontAwesome5 name="shopping-bag" size={size ?? 22} color={focused ? "#007AFF" : "#888"} />
                    ),
                }}
            />
            <Tabs.Screen
                name="profile"
                options={{
                    title: 'PROFILE',
                    tabBarIcon: ({ focused, color, size }) => (
                        <Feather name="user" size={size ?? 24} color={focused ? "#007AFF" : "#888"} />
                    ),
                }}
            />
            {/* Hide these from tab bar */}
            <Tabs.Screen name="chats/index" options={{ href: null }} />
            <Tabs.Screen name="chats/[id]" options={{ href: null }} />
            <Tabs.Screen name="faq" options={{ href: null }} />
        </Tabs>
    );
}
