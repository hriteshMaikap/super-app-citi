import React, { useState } from 'react';
import { View, Text, FlatList, Image, StyleSheet, SafeAreaView, TouchableOpacity, Alert } from 'react-native';
import { useRouter } from 'expo-router';

const initialCartItems = [
    {
        id: '1',
        title: 'Fjallraven Backpack',
        price: 109.95,
        image: 'https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg',
        quantity: 1,
    },
    {
        id: '2',
        title: 'Mens Casual Slim Fit',
        price: 15.99,
        image: 'https://fakestoreapi.com/img/71YXzeOuslL._AC_UY879_.jpg',
        quantity: 1,
    },
    {
        id: '3',
        title: 'Solid Gold Petite Micropave',
        price: 168.0,
        image: 'https://fakestoreapi.com/img/61sbMiUnoGL._AC_UL640_QL65_ML3_.jpg',
        quantity: 1,
    },
];

export default function CartScreen() {
    const [cartItems, setCartItems] = useState(initialCartItems);
    const router = useRouter();

    // Calculate total amount considering quantity
    const totalAmount = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);

    const increaseQuantity = (id) => {
        setCartItems(prev => prev.map(item => item.id === id ? { ...item, quantity: item.quantity + 1 } : item));
    };

    const decreaseQuantity = (id) => {
        setCartItems(prev => prev.map(item => {
            if (item.id === id) {
                const newQuantity = item.quantity - 1;
                return { ...item, quantity: newQuantity > 0 ? newQuantity : 1 };
            }
            return item;
        }));
    };

    const removeItem = (id) => {
        setCartItems(prev => prev.filter(item => item.id !== id));
        Alert.alert('Removed', 'Item removed from cart!');
    };

    const handlePayment = () => {
        router.push('/shopping/Payment');
    };

    const handleGoShopping = () => {
        router.replace('/shopping');
    };

    const renderItem = ({ item }) => (
        <View style={styles.itemContainer}>
            <Image source={{ uri: item.image }} style={styles.image} />
            <View style={styles.infoContainer}>
                <Text style={styles.name}>{item.title}</Text>
                <Text style={styles.price}>${item.price.toFixed(2)}</Text>
                <View style={styles.quantityContainer}>
                    <TouchableOpacity onPress={() => decreaseQuantity(item.id)} style={styles.quantityButton}>
                        <Text style={styles.quantityButtonText}>-</Text>
                    </TouchableOpacity>
                    <Text style={styles.quantityText}>{item.quantity}</Text>
                    <TouchableOpacity onPress={() => increaseQuantity(item.id)} style={styles.quantityButton}>
                        <Text style={styles.quantityButtonText}>+</Text>
                    </TouchableOpacity>
                    <TouchableOpacity onPress={() => removeItem(item.id)} style={styles.removeButton}>
                        <Text style={styles.removeButtonText}>Remove</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </View>
    );

    return (
        <SafeAreaView style={styles.container}>
            {cartItems.length === 0 ? (
                <View style={styles.emptyContainer}>
                    <Text style={styles.emptyText}>Your cart is empty!</Text>
                    <TouchableOpacity
                        style={styles.goShoppingButton}
                        onPress={handleGoShopping}
                    >
                        <Text style={styles.goShoppingButtonText}>Go to Shopping</Text>
                    </TouchableOpacity>
                </View>
            ) : (
                <FlatList
                    data={cartItems}
                    keyExtractor={item => item.id}
                    renderItem={renderItem}
                    contentContainerStyle={styles.listContainer}
                />
            )}
            <View style={styles.totalContainer}>
                <Text style={styles.totalText}>Total: ${totalAmount.toFixed(2)}</Text>
                <TouchableOpacity
                    style={[
                        styles.paymentButton,
                        cartItems.length === 0 && { backgroundColor: '#ccc' }
                    ]}
                    onPress={handlePayment}
                    disabled={cartItems.length === 0}
                >
                    <Text style={styles.paymentButtonText}>Payment</Text>
                </TouchableOpacity>
            </View>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
    },
    listContainer: {
        padding: 16,
    },
    itemContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 16,
    },
    image: {
        width: 60,
        height: 60,
        borderRadius: 8,
        marginRight: 16,
    },
    infoContainer: {
        flex: 1,
    },
    name: {
        fontSize: 16,
        fontWeight: '600',
        marginBottom: 4,
    },
    price: {
        fontSize: 14,
        color: '#888',
    },
    quantityContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        marginTop: 8,
    },
    quantityButton: {
        backgroundColor: '#007AFF',
        borderRadius: 4,
        paddingHorizontal: 10,
        paddingVertical: 4,
        marginRight: 4,
    },
    quantityButtonText: {
        color: '#fff',
        fontSize: 18,
        fontWeight: 'bold',
    },
    quantityText: {
        fontSize: 16,
        marginHorizontal: 8,
        minWidth: 20,
        textAlign: 'center',
    },
    removeButton: {
        backgroundColor: '#FF3B30',
        borderRadius: 4,
        paddingHorizontal: 10,
        paddingVertical: 4,
        marginLeft: 8,
    },
    removeButtonText: {
        color: '#fff',
        fontSize: 13,
        fontWeight: 'bold',
    },
    totalContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: 16,
        borderTopWidth: 1,
        borderTopColor: '#eee',
        backgroundColor: '#f9f9f9',
    },
    totalText: {
        fontSize: 18,
        fontWeight: 'bold',
    },
    paymentButton: {
        backgroundColor: '#0d7f3f',
        borderRadius: 8,
        paddingVertical: 10,
        paddingHorizontal: 24,
        alignItems: 'center',
        justifyContent: 'center',
        elevation: 2,
    },
    paymentButtonText: {
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 16,
        letterSpacing: 0.5,
    },
    emptyContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    emptyText: {
        fontSize: 20,
        color: '#888',
        fontWeight: 'bold',
        marginBottom: 24,
    },
    goShoppingButton: {
        backgroundColor: '#007AFF',
        borderRadius: 8,
        paddingVertical: 12,
        paddingHorizontal: 32,
        marginTop: 12,
    },
    goShoppingButtonText: {
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 16,
    },
});
