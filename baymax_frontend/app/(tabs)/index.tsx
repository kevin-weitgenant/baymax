import React from 'react';
import { View, TextInput, ScrollView, Text, SafeAreaView, StyleSheet, TouchableOpacity } from 'react-native';
import { useChat } from '@ai-sdk/react';
import { fetch as expoFetch } from 'expo/fetch';
import { generateAPIUrl } from '../../utils';
import { Ionicons } from '@expo/vector-icons';

type Message = {
  id: string;
  role: string;
  content: string;
};

export default function ChatScreen() {
  const { messages, error, handleInputChange, input, handleSubmit } = useChat({
    fetch: expoFetch as unknown as typeof globalThis.fetch,
    api: generateAPIUrl('/api/chat'),
    onError: (error: Error) => console.error(error, 'ERROR'),
  });

  if (error) return <Text style={styles.errorText}>{error.message}</Text>;

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.chatContainer}>
        <ScrollView style={styles.messageList}>
          {messages.map((m: Message) => (
            <View key={m.id} style={{ marginVertical: 8 }}>
              <View>
                <Text style={styles.messageRole}>{m.role}</Text>
                <Text style={styles.messageContent}>{m.content}</Text>
              </View>
            </View>
          ))}
        </ScrollView>

        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="Say something..."
            value={input}
            onChange={e =>
              handleInputChange({
                ...e,
                target: {
                  ...e.target,
                  value: e.nativeEvent.text,
                },
              } as unknown as React.ChangeEvent<HTMLInputElement>)
            }
            onSubmitEditing={e => {
              handleSubmit(e);
              e.preventDefault();
            }}
            autoFocus={true}
          />
          <TouchableOpacity style={styles.photoButton} onPress={() => console.log('Photo upload')}>
            <Ionicons name="camera" size={24} color="#007AFF" />
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    height: "100%",
  },
  chatContainer: {
    backgroundColor: "white",
    height: "95%",
    display: "flex",
    flexDirection: "column",
    paddingHorizontal: 8,
  },
  messageList: {
    flex: 1,
  },
  messageRole: {
    fontWeight: "700",
    marginBottom: 4,
  },
  messageContent: {
    fontSize: 16,
  },
  inputContainer: {
    marginTop: 8,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'center',
  },
  input: {
    backgroundColor: "white",
    padding: 8,
    borderRadius: 8,
    borderColor: "#ddd",
    borderWidth: 1,
    flex: 1,
    marginRight: 8,
  },
  photoButton: {
    padding: 8,
    borderRadius: 8,
    borderColor: "#ddd",
    borderWidth: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  errorText: {
    color: "red",
    padding: 20,
    textAlign: "center",
  },
});
