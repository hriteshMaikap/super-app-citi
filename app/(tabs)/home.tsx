import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import { Ionicons, MaterialIcons, FontAwesome5, MaterialCommunityIcons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

export default function HomeScreen() {
    const router = useRouter();

    const features = [
        {
            title: 'Shopping',
            icon: <FontAwesome5 name="shopping-bag" size={24} color="#007AFF" />,
            screen: '/shopping'
        },
        {
            title: 'Wallet',
            icon: <Ionicons name="wallet" size={24} color="#007AFF" />,
            screen: '/wallet'
        },
        {
            title: 'Payments',
            icon: <MaterialIcons name="payment" size={24} color="#007AFF" />,
            screen: '/payments'
        },
        {
            title: 'Chat',
            icon: <Ionicons name="chatbubble-ellipses" size={24} color="#007AFF" />,
            screen: '/chat'
        },
    ];

    const quickActions = [
        {
            title: 'Pay Bills',
            icon: <MaterialCommunityIcons name="file-document" size={24} color="#4CAF50" />,
            screen: '/bills'
        },
        {
            title: 'Account Status',
            icon: <MaterialIcons name="account-balance" size={24} color="#FF9800" />,
            screen: '/account-status'
        },
        {
            title: 'Transaction History',
            icon: <MaterialCommunityIcons name="history" size={24} color="#9C27B0" />,
            screen: '/transactions'
        },
        {
            title: 'Recharge',
            icon: <Ionicons name="phone-portrait" size={24} color="#E91E63" />,
            screen: '/recharge'
        },
    ];

    return (
        <ScrollView contentContainerStyle={styles.container}>
            {/* Header */}
            <View style={styles.header}>
                <Text style={styles.headerTitle}>My Finance App</Text>
            </View>

            {/* Balance Card */}
            <TouchableOpacity
                style={styles.balanceCard}
                onPress={() => router.push('/wallet')}
            >
                <View style={styles.balanceContent}>
                    <Text style={styles.balanceLabel}>Current Balance</Text>
                    <Text style={styles.balanceAmount}>₹25,456.00</Text>
                </View>
                <Ionicons name="chevron-forward" size={24} color="#666" />
            </TouchableOpacity>

            {/* Features Grid */}
            <View style={styles.grid}>
                {features.map((feature, index) => (
                    <TouchableOpacity
                        key={index}
                        style={styles.card}
                        onPress={() => router.push(feature.screen)}
                    >
                        <View style={styles.cardContent}>
                            {feature.icon}
                            <Text style={styles.cardTitle}>{feature.title}</Text>
                        </View>
                    </TouchableOpacity>
                ))}
            </View>

            {/* Quick Actions Grid */}
            <Text style={styles.sectionTitle}>Quick Actions</Text>
            <View style={styles.grid}>
                {quickActions.map((action, index) => (
                    <TouchableOpacity
                        key={index}
                        style={[styles.card, styles.quickActionCard]}
                        onPress={() => router.push(action.screen)}
                    >
                        <View style={styles.cardContent}>
                            {action.icon}
                            <Text style={styles.quickActionTitle}>{action.title}</Text>
                        </View>
                    </TouchableOpacity>
                ))}
            </View>

            {/* SDK Section */}
            <View style={styles.sdkSection}>
                <Text style={styles.sectionTitle}>Integration SDKs</Text>
                <View style={[styles.card, styles.sdkCard]}>
                    <View style={styles.cardContent}>
                        <MaterialCommunityIcons name="developer-board" size={24} color="#666" />
                        <View style={styles.sdkTextContainer}>
                            <Text style={styles.sdkTitle}>Payment Gateway SDK</Text>
                            <Text style={styles.sdkSubtitle}>Easy integration with major payment providers</Text>
                        </View>
                        <View style={styles.comingSoonBadge}>
                            <Text style={styles.comingSoonText}>Coming Soon</Text>
                        </View>
                    </View>
                </View>
            </View>
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    container: {
        flexGrow: 1,
        padding: 16,
        backgroundColor: '#f8f9fa'
    },
    header: {
        marginBottom: 24,
        paddingHorizontal: 8
    },
    headerTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#1a1a1a',
        marginBottom: 4
    },
    balanceCard: {
        backgroundColor: '#fff',
        borderRadius: 12,
        padding: 20,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: 20,
        elevation: 2,
        shadowColor: '#000',
        shadowOpacity: 0.05,
        shadowRadius: 8,
        shadowOffset: { width: 0, height: 2 }
    },
    balanceContent: {
        flex: 1,
    },
    balanceLabel: {
        fontSize: 16,
        color: '#666',
        marginBottom: 4
    },
    balanceAmount: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#2e7d32'
    },
    grid: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: 12,
        marginBottom: 20
    },
    card: {
        width: '48%',
        backgroundColor: '#fff',
        borderRadius: 12,
        padding: 16,
        elevation: 2,
        shadowColor: '#000',
        shadowOpacity: 0.05,
        shadowRadius: 8,
        shadowOffset: { width: 0, height: 2 }
    },
    quickActionCard: {
        backgroundColor: '#f8f9fa',
    },
    cardContent: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 12
    },
    cardTitle: {
        flex: 1,
        fontSize: 16,
        fontWeight: '500',
        color: '#333'
    },
    quickActionTitle: {
        flex: 1,
        fontSize: 14,
        fontWeight: '500',
        color: '#444'
    },
    sectionTitle: {
        fontSize: 20,
        fontWeight: 'bold',
        color: '#1a1a1a',
        marginBottom: 16,
        paddingHorizontal: 8
    },
    sdkSection: {
        marginTop: 24
    },
    sdkCard: {
        width: '100%',
        backgroundColor: '#f3f4f6'
    },
    sdkTextContainer: {
        flex: 1,
        gap: 2
    },
    sdkTitle: {
        fontSize: 16,
        fontWeight: '500',
        color: '#333'
    },
    sdkSubtitle: {
        fontSize: 12,
        color: '#666'
    },
    comingSoonBadge: {
        backgroundColor: '#e5e7eb',
        borderRadius: 6,
        paddingVertical: 4,
        paddingHorizontal: 8
    },
    comingSoonText: {
        fontSize: 10,
        fontWeight: '500',
        color: '#666'
    }
});
