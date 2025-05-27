import React, { useState } from 'react';
import {
    View,
    Text,
    FlatList,
    Image,
    TouchableOpacity,
    StyleSheet,
    SafeAreaView,
    Alert,
    TextInput
} from 'react-native';
import { shopData, Product } from '../../data/shopData';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

type CartItem = {
    product: Product;
    quantity: number;
};

export default function ShoppingScreen() {
    const [cart, setCart] = useState<CartItem[]>([]);
    const [searchQuery, setSearchQuery] = useState('');
    const router = useRouter();

    // Filter products based on search query
    const filteredProducts = shopData.filter(product => {
        const lowerQuery = searchQuery.toLowerCase();
        return (
            product.title.toLowerCase().includes(lowerQuery) ||
            product.category.toLowerCase().includes(lowerQuery)
        );
    });

    const getCartItem = (productId: number) => cart.find(item => item.product.id === productId);

    const addToCart = (product: Product) => {
        setCart(prev => {
            const existing = prev.find(item => item.product.id === product.id);
            if (existing) {
                return prev.map(item =>
                    item.product.id === product.id
                        ? { ...item, quantity: item.quantity + 1 }
                        : item
                );
            }
            return [...prev, { product, quantity: 1 }];
        });
        Alert.alert('Added to Cart', `${product.title} added to cart!`);
    };

    const decreaseQuantity = (productId: number) => {
        setCart(prev =>
            prev
                .map(item =>
                    item.product.id === productId
                        ? { ...item, quantity: item.quantity - 1 }
                        : item
                )
                .filter(item => item.quantity > 0)
        );
    };

    const removeFromCart = (productId: number) => {
        setCart(prev => prev.filter(item => item.product.id !== productId));
        Alert.alert('Removed from Cart', 'Item removed from cart!');
    };

    const totalCartItems = cart.reduce((sum, item) => sum + item.quantity, 0);

    const renderProductCard = ({ item }: { item: Product }) => {
        const cartItem = getCartItem(item.id);
        const inCart = !!cartItem;

        return (
            <View style={styles.productCard}>
                <Image source={{ uri: item.image }} style={styles.productImage} />

                <View style={styles.productInfo}>
                    <Text style={styles.productTitle} numberOfLines={2}>
                        {item.title}
                    </Text>

                    <Text style={styles.productPrice}>${item.price}</Text>

                    <View style={styles.ratingContainer}>
                        <Text style={styles.rating}>Rating: {item.rating.rate}</Text>
                        <Text style={styles.ratingCount}>({item.rating.count})</Text>
                    </View>

                    <Text style={styles.category}>{item.category}</Text>

                    {inCart ? (
                        <>
                            <View style={styles.quantityContainer}>
                                <TouchableOpacity
                                    style={styles.quantityButton}
                                    onPress={() => decreaseQuantity(item.id)}
                                >
                                    <Text style={styles.quantityButtonText}>-</Text>
                                </TouchableOpacity>

                                <Text style={styles.quantityText}>{cartItem.quantity}</Text>

                                <TouchableOpacity
                                    style={styles.quantityButton}
                                    onPress={() => addToCart(item)}
                                >
                                    <Text style={styles.quantityButtonText}>+</Text>
                                </TouchableOpacity>
                            </View>
                            <TouchableOpacity
                                style={styles.removeButton}
                                onPress={() => removeFromCart(item.id)}
                            >
                                <Text style={styles.cartButtonText}>Remove from Cart</Text>
                            </TouchableOpacity>
                        </>
                    ) : (
                        <TouchableOpacity
                            style={styles.addButton}
                            onPress={() => addToCart(item)}
                        >
                            <Ionicons name="cart-outline" size={18} color="#fff" style={{ marginRight: 6 }} />
                            <Text style={styles.cartButtonText}>Add to Cart</Text>
                        </TouchableOpacity>
                    )}
                </View>
            </View>
        );
    };

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.header}>
                {/*<Text style={styles.headerTitle}>Shop</Text>*/}
                <View style={styles.searchCartContainer}>
                    <TextInput
                        style={styles.searchInput}
                        placeholder="Search products or categories..."
                        value={searchQuery}
                        onChangeText={setSearchQuery}
                    />
                    <TouchableOpacity onPress={() => router.push('/shopping/Cart')} style={styles.cartIconButton}>
                        <Ionicons name="cart" size={28} color="#007AFF" />
                        {totalCartItems > 0 && (
                            <View style={styles.cartBadge}>
                                <Text style={styles.cartBadgeText}>{totalCartItems}</Text>
                            </View>
                        )}
                    </TouchableOpacity>
                </View>
            </View>

            <FlatList
                data={filteredProducts}
                renderItem={renderProductCard}
                keyExtractor={(item) => item.id.toString()}
                numColumns={2}
                contentContainerStyle={styles.productList}
                columnWrapperStyle={styles.row}
                showsVerticalScrollIndicator={false}
            />
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f5f5f5',
    },
    header: {
        padding: 16,
        backgroundColor: '#fff',
        elevation: 2,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
    },
    headerTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#333',
        marginBottom: 12,
    },
    searchCartContainer: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    searchInput: {
        flex: 1,
        height: 40,
        borderColor: '#ddd',
        borderWidth: 1,
        borderRadius: 20,
        paddingHorizontal: 16,
        backgroundColor: '#fff',
    },
    cartIconButton: {
        marginLeft: 12,
        padding: 6,
        position: 'relative',
    },
    cartBadge: {
        position: 'absolute',
        top: -4,
        right: -4,
        backgroundColor: '#FF3B30',
        borderRadius: 8,
        paddingHorizontal: 5,
        paddingVertical: 1,
        minWidth: 16,
        alignItems: 'center',
        justifyContent: 'center',
    },
    cartBadgeText: {
        color: '#fff',
        fontSize: 10,
        fontWeight: 'bold',
    },
    productList: {
        padding: 8,
    },
    row: {
        justifyContent: 'space-between',
    },
    productCard: {
        backgroundColor: '#fff',
        borderRadius: 12,
        margin: 6,
        width: '48%',
        elevation: 3,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        overflow: 'hidden',
    },
    productImage: {
        width: '100%',
        height: 150,
        resizeMode: 'contain',
        backgroundColor: '#f9f9f9',
    },
    productInfo: {
        padding: 12,
    },
    productTitle: {
        fontSize: 14,
        fontWeight: '600',
        color: '#333',
        marginBottom: 8,
        lineHeight: 18,
    },
    productPrice: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#007AFF',
        marginBottom: 6,
    },
    ratingContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 6,
    },
    rating: {
        fontSize: 14,
        color: '#ff9500',
        fontWeight: '600',
    },
    ratingCount: {
        fontSize: 12,
        color: '#666',
        marginLeft: 4,
    },
    category: {
        fontSize: 12,
        color: '#888',
        textTransform: 'uppercase',
        marginBottom: 12,
    },
    cartButton: {
        borderRadius: 8,
        paddingVertical: 10,
        paddingHorizontal: 12,
        alignItems: 'center',
        flexDirection: 'row',
        justifyContent: 'center',
    },
    addButton: {
        backgroundColor: '#0d7f3f',
        borderRadius: 12,
        paddingVertical: 12,
        paddingHorizontal: 18,
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'row',
        marginTop: 8,
        shadowColor: '#0d7f3f',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.15,
        shadowRadius: 6,
        elevation: 4,
    },
    removeButton: {
        backgroundColor: '#FF3B30',
        borderRadius: 8,
        paddingVertical: 10,
        paddingHorizontal: 12,
        alignItems: 'center',
        marginTop: 8,
    },
    cartButtonText: {
        color: '#fff',
        fontSize: 16,
        fontWeight: 'bold',
        textAlign: 'center',
        letterSpacing: 0.5,
    },
    quantityContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        marginTop: 8,
        marginBottom: 4,
    },
    quantityButton: {
        backgroundColor: '#007AFF',
        width: 32,
        height: 32,
        borderRadius: 16,
        justifyContent: 'center',
        alignItems: 'center',
    },
    quantityButtonText: {
        color: '#fff',
        fontSize: 18,
        fontWeight: 'bold',
    },
    quantityText: {
        fontSize: 16,
        marginHorizontal: 12,
        minWidth: 20,
        textAlign: 'center',
    },
});
