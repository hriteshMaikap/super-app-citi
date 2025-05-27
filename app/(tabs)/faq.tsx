import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView, LayoutAnimation, Platform, UIManager } from 'react-native';
import { AntDesign } from '@expo/vector-icons';

// Enable LayoutAnimation on Android
if (Platform.OS === 'android' && UIManager.setLayoutAnimationEnabledExperimental) {
    UIManager.setLayoutAnimationEnabledExperimental(true);
}

const FAQ_DATA = [
    {
        question: 'How do I reset my password?',
        answer: 'Go to the login screen, tap "Forgot Password", and follow the instructions to reset your password via email.',
    },
    {
        question: 'How can I contact support?',
        answer: 'You can contact support via the "Contact Us" page in your profile tab or email us at support@example.com.',
    },
    {
        question: 'Where can I view my purchase history?',
        answer: 'Your purchase history is available in the "Payments" tab under "Transaction History".',
    },
    {
        question: 'How do I update my profile information?',
        answer: 'Go to the Profile tab and tap "Edit Profile" to update your details.',
    },
    {
        question: 'Is my data secure?',
        answer: 'Yes, we use industry-standard encryption to keep your data safe and secure.',
    },
];

export default function FAQScreen() {
    const [expandedIndexes, setExpandedIndexes] = useState<number[]>([]);

    const toggleExpand = (index: number) => {
        LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
        setExpandedIndexes((prev) =>
            prev.includes(index)
                ? prev.filter((i) => i !== index)
                : [...prev, index]
        );
    };

    return (
        <ScrollView contentContainerStyle={styles.container}>
            <Text style={styles.header}>Frequently Asked Questions</Text>
            {FAQ_DATA.map((item, idx) => {
                const expanded = expandedIndexes.includes(idx);
                return (
                    <View key={idx} style={styles.card}>
                        <TouchableOpacity
                            style={styles.questionRow}
                            onPress={() => toggleExpand(idx)}
                            activeOpacity={0.8}
                        >
                            <Text style={styles.question}>{item.question}</Text>
                            <AntDesign
                                name={expanded ? 'down' : 'right'}
                                size={20}
                                color="#333"
                            />
                        </TouchableOpacity>
                        {expanded && (
                            <View style={styles.answerBox}>
                                <Text style={styles.answer}>{item.answer}</Text>
                            </View>
                        )}
                    </View>
                );
            })}
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    container: {
        padding: 16,
        paddingBottom: 32,
        backgroundColor: '#f9f9f9',
    },
    header: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 24,
        textAlign: 'center',
    },
    card: {
        backgroundColor: '#fff',
        borderRadius: 10,
        marginBottom: 16,
        paddingHorizontal: 16,
        paddingVertical: 4,
        elevation: 2,
        shadowColor: '#000',
        shadowOpacity: 0.07,
        shadowRadius: 4,
        shadowOffset: { width: 0, height: 2 },
    },
    questionRow: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingVertical: 16,
    },
    question: {
        fontSize: 16,
        fontWeight: '600',
        color: '#222',
        flex: 1,
        paddingRight: 8,
    },
    answerBox: {
        borderTopWidth: 1,
        borderTopColor: '#eee',
        paddingVertical: 12,
    },
    answer: {
        fontSize: 15,
        color: '#444',
        lineHeight: 22,
    },
});
